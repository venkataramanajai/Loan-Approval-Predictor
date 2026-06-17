import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score

def clean_and_feature_engineer(df):
    df = df.copy()
    
    # 1. Convert Dependents to numeric (handling '3+')
    df['Dependents'] = df['Dependents'].replace('3+', 3)
    df['Dependents'] = pd.to_numeric(df['Dependents'], errors='coerce')
    # We will impute Dependents missing values with 0
    df['Dependents'] = df['Dependents'].fillna(0)
    
    # 2. Total Income
    df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    
    # 3. Debt to Income Ratio (assuming LoanAmount is in thousands, so we scale it)
    # LoanAmount is usually represented in thousands, ApplicantIncome is monthly.
    # Monthly loan repayment approximation: LoanAmount * 1000 / Loan_Amount_Term
    # We can create a simpler ratio: LoanAmount * 1000 / (Total_Income + 1)
    df['Loan_to_Income_Ratio'] = (df['LoanAmount'] * 1000) / (df['Total_Income'] + 1)
    
    # 4. Income per Dependent
    df['Income_Per_Dependent'] = df['Total_Income'] / (df['Dependents'] + 1)
    
    return df

def main():
    print("Loading data...")
    # Load dataset
    data_path = os.path.join("data", "train_u6lujuX_CVtuZ9i (1).csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
        
    df = pd.read_csv(data_path)
    
    # Drop Loan_ID
    if 'Loan_ID' in df.columns:
        df = df.drop(columns=['Loan_ID'])
        
    # Map target variable Loan_Status (Y -> 1, N -> 0)
    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})
    
    # Separate features and target
    X = df.drop(columns=['Loan_Status'])
    y = df['Loan_Status']
    
    # Clean and engineer features
    print("Engineering features...")
    X = clean_and_feature_engineer(X)
    
    # Define features
    numerical_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 
                      'Loan_Amount_Term', 'Total_Income', 'Loan_to_Income_Ratio', 
                      'Income_Per_Dependent', 'Dependents']
    categorical_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 
                        'Credit_History', 'Property_Area']
    
    # Preprocessing pipelines
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Define models to train
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(random_state=42, eval_metric='logloss')
    }
    
    best_model = None
    best_f1 = 0
    best_model_name = ""
    trained_pipelines = {}
    
    print("\nTraining models...")
    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"Model: {name}")
        print(f"  Accuracy: {acc:.4f}")
        print(f"  F1 Score: {f1:.4f}")
        print(classification_report(y_test, y_pred))
        
        trained_pipelines[name] = pipeline
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = pipeline
            best_model_name = name
            
    print(f"\nBest Model: {best_model_name} with F1-score {best_f1:.4f}")
    
    # Save best model
    os.makedirs("models", exist_ok=True)
    model_save_path = os.path.join("models", "best_model.joblib")
    joblib.dump(best_model, model_save_path)
    print(f"Saved best model to {model_save_path}")
    
    # Save the feature names and columns expected
    feature_meta = {
        'numerical_cols': numerical_cols,
        'categorical_cols': categorical_cols,
        'model_name': best_model_name
    }
    joblib.dump(feature_meta, os.path.join("models", "feature_meta.joblib"))
    print("Saved feature metadata.")

if __name__ == "__main__":
    main()
