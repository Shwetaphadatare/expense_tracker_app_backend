from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_expenses: float
    total_transactions: int
    
class CategoryBreakdown(BaseModel):
    category: str
    total_amount: float
    
class MonthlyBreakdown(BaseModel):
    month: str
    total_amount:float
    
