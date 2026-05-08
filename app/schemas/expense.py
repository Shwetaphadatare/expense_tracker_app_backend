from pydantic import BaseModel, Field

class ExpenseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    amount: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=50)
    
class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    
    class Config:
        from_attributes = True
    