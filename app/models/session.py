from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Boolean
from datetime import datetime

from app.db.base_class import Base

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    refresh_token = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    is_revoked = Column(Boolean,default=False)