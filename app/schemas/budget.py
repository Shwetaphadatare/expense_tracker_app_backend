from pydantic import BaseModel, Field, field_validator
import re
from app.models.enums import ExpenseCategoryEnum

class BudgetCreate(BaseModel):
    category: ExpenseCategoryEnum
    monthly_limit: float = Field(gt=0)
    month: str

    @field_validator("month")
    @classmethod
    def validate_month(cls, value):
        if not re.match(r"^\d{4}-\d{2}$", value):
            raise ValueError(
                "Month must be in YYYY-MM format (example: 2026-05)"
            )

        year, month = value.split("-")

        if int(month) < 1 or int(month) > 12:
            raise ValueError(
                "Month must be between 01 and 12"
            )

        return value
    
class BudgetResponse(BaseModel):
    id : int
    category:ExpenseCategoryEnum
    monthly_limit : float
    month:str
    
    class Config:
        from_attributes = True
        
class BudgetAlert(BaseModel):
    category:ExpenseCategoryEnum
    monthly_limit:float
    spent:float
    remaining:float
    status:str
    
    
class BudgetUpdate(BaseModel):
    category: ExpenseCategoryEnum
    monthly_limit: float = Field(gt=0)
    month:str
    
    