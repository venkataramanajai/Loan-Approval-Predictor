import os
import sys
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# Add parent directory to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import models, schemas
from backend.database import engine, get_db

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loan Approval Predictor API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model and feature metadata
MODEL_PATH = os.path.join("models", "best_model.joblib")
META_PATH = os.path.join("models", "feature_meta.joblib")

model = None
feature_meta = None

@app.on_event("startup")
def load_model():
    global model, feature_meta
    if os.path.exists(MODEL_PATH) and os.path.exists(META_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            feature_meta = joblib.load(META_PATH)
            print(f"Model loaded successfully: {feature_meta['model_name']}")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print("Model file not found. Please run ml/train.py first.")

# In-memory simple caching to mimic Redis
# Keys: tuple of application features, Values: (prediction, probability, timestamp)
prediction_cache = {}

def clean_and_engineer_single(data: schemas.LoanApplicationCreate):
    # Convert Dependents mapping
    deps = data.dependents if data.dependents is not None else 0
    
    total_income = data.applicant_income + data.coapplicant_income
    
    # Calculate loan to income ratio (loan amount is in thousands, so scale by 1000)
    loan_amt = data.loan_amount if data.loan_amount is not None else 0
    loan_to_income_ratio = (loan_amt * 1000) / (total_income + 1)
    
    income_per_dependent = total_income / (deps + 1)
    
    return {
        'total_income': total_income,
        'loan_to_income_ratio': loan_to_income_ratio,
        'income_per_dependent': income_per_dependent,
        'dependents_processed': deps
    }

@app.post("/api/predict", response_model=schemas.LoanApplicationResponse)
def predict_loan(application: schemas.LoanApplicationCreate, db: Session = Depends(get_db)):
    if model is None:
        raise HTTPException(status_code=503, detail="Machine learning model is not loaded.")
    
    # Cache key based on fields
    cache_key = (
        application.gender,
        application.married,
        application.dependents,
        application.education,
        application.self_employed,
        application.applicant_income,
        application.coapplicant_income,
        application.loan_amount,
        application.loan_amount_term,
        application.credit_history,
        application.property_area
    )
    
    # Check cache (mimics Redis)
    if cache_key in prediction_cache:
        cached_result = prediction_cache[cache_key]
        print("Returning cached prediction!")
        
        # Save to database anyway for history tracking
        db_app = models.LoanApplication(
            gender=application.gender,
            married=application.married,
            dependents=application.dependents or 0,
            education=application.education,
            self_employed=application.self_employed,
            applicant_income=application.applicant_income,
            coapplicant_income=application.coapplicant_income,
            loan_amount=application.loan_amount,
            loan_amount_term=application.loan_amount_term,
            credit_history=application.credit_history,
            property_area=application.property_area,
            total_income=cached_result['total_income'],
            loan_to_income_ratio=cached_result['loan_to_income_ratio'],
            income_per_dependent=cached_result['income_per_dependent'],
            prediction=cached_result['prediction'],
            probability=cached_result['probability'],
            status=cached_result['status']
        )
        db.add(db_app)
        db.commit()
        db.refresh(db_app)
        return db_app

    # Calculate engineered features
    features = clean_and_engineer_single(application)
    
    # Build dataframe for model prediction
    # Ensure column order matches columns during fit
    input_data = pd.DataFrame([{
        'ApplicantIncome': application.applicant_income,
        'CoapplicantIncome': application.coapplicant_income,
        'LoanAmount': application.loan_amount,
        'Loan_Amount_Term': application.loan_amount_term,
        'Total_Income': features['total_income'],
        'Loan_to_Income_Ratio': features['loan_to_income_ratio'],
        'Income_Per_Dependent': features['income_per_dependent'],
        'Dependents': features['dependents_processed'],
        'Gender': application.gender,
        'Married': application.married,
        'Education': application.education,
        'Self_Employed': application.self_employed,
        'Credit_History': application.credit_history,
        'Property_Area': application.property_area
    }])
    
    # Run prediction
    try:
        prediction_val = int(model.predict(input_data)[0])
        probabilities = model.predict_proba(input_data)[0]
        probability_val = float(probabilities[1])  # probability of Y
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {str(e)}")
        
    status_str = "Approved" if prediction_val == 1 else "Rejected"
    
    # Save cache
    prediction_cache[cache_key] = {
        'total_income': features['total_income'],
        'loan_to_income_ratio': features['loan_to_income_ratio'],
        'income_per_dependent': features['income_per_dependent'],
        'prediction': prediction_val,
        'probability': probability_val,
        'status': status_str
    }
    
    # Save to Database
    db_app = models.LoanApplication(
        gender=application.gender,
        married=application.married,
        dependents=application.dependents or 0,
        education=application.education,
        self_employed=application.self_employed,
        applicant_income=application.applicant_income,
        coapplicant_income=application.coapplicant_income,
        loan_amount=application.loan_amount,
        loan_amount_term=application.loan_amount_term,
        credit_history=application.credit_history,
        property_area=application.property_area,
        total_income=features['total_income'],
        loan_to_income_ratio=features['loan_to_income_ratio'],
        income_per_dependent=features['income_per_dependent'],
        prediction=prediction_val,
        probability=probability_val,
        status=status_str
    )
    
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    
    return db_app

@app.get("/api/history", response_model=List[schemas.LoanApplicationResponse])
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.LoanApplication).order_by(models.LoanApplication.applied_at.desc()).limit(limit).all()

@app.get("/api/stats", response_model=schemas.DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    applications = db.query(models.LoanApplication).all()
    total = len(applications)
    
    if total == 0:
        return schemas.DashboardStats(
            total_applications=0,
            approval_rate=0.0,
            approved_count=0,
            rejected_count=0,
            average_income=0.0,
            average_loan_amount=0.0
        )
        
    approved = sum(1 for app in applications if app.prediction == 1)
    rejected = total - approved
    approval_rate = approved / total
    
    avg_income = sum(app.applicant_income for app in applications) / total
    
    loan_amounts = [app.loan_amount for app in applications if app.loan_amount is not None]
    avg_loan = sum(loan_amounts) / len(loan_amounts) if loan_amounts else 0.0
    
    return schemas.DashboardStats(
        total_applications=total,
        approval_rate=approval_rate,
        approved_count=approved,
        rejected_count=rejected,
        average_income=avg_income,
        average_loan_amount=avg_loan
    )

@app.get("/api/explain/{application_id}")
def explain_loan(application_id: int, db: Session = Depends(get_db)):
    application = db.query(models.LoanApplication).filter(models.LoanApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    # Build simple explainability list based on rules & weights of logistic regression
    explanations = []
    
    # 1. Credit History is the single most important feature in this dataset
    if application.credit_history == 1.0:
        explanations.append({
            "factor": "Credit History",
            "impact": "Positive",
            "score": 0.8,
            "description": "Applicant meets the prime credit history guidelines, which strongly suggests reliability."
        })
    else:
        explanations.append({
            "factor": "Credit History",
            "impact": "Negative",
            "score": -0.9,
            "description": "Applicant has an insufficient or poor credit history record. This is a critical risk factor."
        })
        
    # 2. Loan to Income Ratio
    if application.loan_to_income_ratio > 300:
        explanations.append({
            "factor": "Debt-to-Income",
            "impact": "Negative",
            "score": -0.6,
            "description": f"The requested loan relative to monthly income ({application.loan_to_income_ratio:.1f}%) is high, creating repayment strain."
        })
    elif application.loan_to_income_ratio < 100:
        explanations.append({
            "factor": "Debt-to-Income",
            "impact": "Positive",
            "score": 0.5,
            "description": f"Low Loan-to-Income ratio ({application.loan_to_income_ratio:.1f}%) indicates a comfortable capacity for repayment."
        })
        
    # 3. Income per Dependent
    if application.dependents > 0 and application.income_per_dependent < 1500:
        explanations.append({
            "factor": "Income Per Dependent",
            "impact": "Negative",
            "score": -0.3,
            "description": f"Available monthly income per dependent (₹{application.income_per_dependent:.2f}) is low, increasing household financial pressure."
        })
    elif application.income_per_dependent > 5000:
        explanations.append({
            "factor": "Income Stability",
            "impact": "Positive",
            "score": 0.4,
            "description": f"High disposable income per dependent (₹{application.income_per_dependent:.2f}) suggests excellent financial cushioning."
        })
        
    # 4. Property Area
    if application.property_area == "Semiurban":
        explanations.append({
            "factor": "Property Location",
            "impact": "Positive",
            "score": 0.2,
            "description": "Loans in semiurban areas have historically higher approval rates due to favorable market valuations."
        })
        
    # 5. Education
    if application.education == "Graduate":
        explanations.append({
            "factor": "Educational Background",
            "impact": "Positive",
            "score": 0.1,
            "description": "Applicant is a graduate, which correlates statistically with career progression and income stability."
        })
        
    return {
        "status": application.status,
        "probability": application.probability,
        "explanations": explanations
    }
