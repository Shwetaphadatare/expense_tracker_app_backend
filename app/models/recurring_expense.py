from sqlalchemy import Column, Integer,String, Float,DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

class RecurringExpense(Base):
    __tablename__ = "recurring_expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    title = Column(String, nullable=False)
    
    amount = Column(Float, nullable=False)
    
    category = Column(String, nullable=False)
    
    frequency = Column(String,nullable=False)
    
    next_due_date = Column(DateTime, nullable=False)
    
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    
    created_at = Column(DateTime,
                        default=datetime.now)
    
    owner = relationship("User")
    
    
    