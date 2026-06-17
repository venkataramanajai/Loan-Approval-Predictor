from pydantic import BaseModel, Field
from typing import Optional
import datetime

class LoanApplicationBase(BaseModel):
    gender: Optional[str] = Field(None, description="Gender of applicant (Male, Female)")
    married: Optional[str] = Field(None, description="Married status (Yes, No)")
    dependents: Optional[int] = Field(0, description="Number of dependents (0, 1, 2, 3)")
    education: str = Field(..., description="Education status (Graduate, Not Graduate)")
    self_employed: Optional[str] = Field(None, description="Self employed (Yes, No)")
    applicant_income: float = Field(..., description="Applicant monthly income")
    coapplicant_income: float = Field(0.0, description="Co-applicant monthly income")
    loan_amount: Optional[float] = Field(None, description="Loan amount in thousands")
    loan_amount_term: Optional[float] = Field(360.0, description="Term of loan in months")
    credit_history: Optional[float] = Field(1.0, description="Credit history (1.0 = meets guidelines, 0.0 = does not meet)")
    property_area: str = Field(..., description="Property area (Urban, Semiurban, Rural)")

class LoanApplicationCreate(LoanApplicationBase):
    pass

class LoanApplicationResponse(LoanApplicationBase):
    id: int
    total_income: float
    loan_to_income_ratio: float
    income_per_dependent: float
    prediction: int
    probability: float
    status: str
    applied_at: datetime.datetime

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_applications: int
    approval_rate: float
    approved_count: int
    rejected_count: int
    average_income: float
    average_loan_amount: float
