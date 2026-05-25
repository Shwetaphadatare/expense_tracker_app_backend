from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.enums import ExpenseCategoryEnum

class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(Enum(ExpenseCategoryEnum), nullable=False)
    monthly_limit = Column(Float, nullable=False)
    month = Column(String(7), nullable=False)
    
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    
    owner = relationship("User")