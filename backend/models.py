from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime
from .database import Base

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String, nullable=True)
    married = Column(String, nullable=True)
    dependents = Column(Integer, default=0)
    education = Column(String, nullable=False)
    self_employed = Column(String, nullable=True)
    applicant_income = Column(Float, nullable=False)
    coapplicant_income = Column(Float, nullable=False)
    loan_amount = Column(Float, nullable=True)
    loan_amount_term = Column(Float, nullable=True)
    credit_history = Column(Float, nullable=True)
    property_area = Column(String, nullable=False)
    
    # Calculated/engineered features stored for audit/reference
    total_income = Column(Float, nullable=True)
    loan_to_income_ratio = Column(Float, nullable=True)
    income_per_dependent = Column(Float, nullable=True)
    
    # ML Prediction outputs
    prediction = Column(Integer, nullable=False)  # 1 for Yes, 0 for No
    probability = Column(Float, nullable=False)   # Probability of approval
    status = Column(String, nullable=False)       # "Approved" or "Rejected"
    
    applied_at = Column(DateTime, default=datetime.datetime.utcnow)
