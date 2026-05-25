from sqlalchemy import Column, Integer,String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
 
from app.db.base import Base
from app.models.enums import ExpenseCategoryEnum


class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True,index=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Enum(ExpenseCategoryEnum), nullable=False)
    
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    
    created_at = Column(DateTime, default=datetime.now,nullable=False)
    
    owner = relationship("User")
    
    