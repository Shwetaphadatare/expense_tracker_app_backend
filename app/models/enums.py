from enum import Enum

class ExpenseCategoryEnum(str, Enum):
    food = "food"
    travel = "travel"
    bills = "bills"
    shopping = "shopping"
    health = "health"
    entertainment = "entertainment"
    other = "other"
    
class FrequencyEnum(str, Enum):
    monthly = "monthly"
    weekly = "weekly"
    
