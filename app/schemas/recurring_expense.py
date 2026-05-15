from pydantic import BaseModel, Field
from datetime import datetime

class RecurringExpenseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    amount: float = Field(gt=0)
    category:str = Field(min_length=2, max_length=50)
    frequency:str
    next_due_date: datetime
    

class RecurringExpenseResponse(BaseModel):
    id:int
    title:str
    amount:float
    category:str
    frequency:str
    next_due_date: datetime
    
    class Config:
        from_attributes = True
        