from pydantic import BaseModel, Field
from datetime import datetime
from app.models.enums import ExpenseCategoryEnum

class ExpenseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    amount: float = Field(gt=0)
    category: ExpenseCategoryEnum
    
class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: ExpenseCategoryEnum
    created_at: datetime
    
    class Config:
        from_attributes = True
    
class ExpenseUpdate(BaseModel):
    title:str = Field(min_length=2, max_length=100)
    amount:float = Field(gt=0)
    category: ExpenseCategoryEnum
    
    
