from fastapi import FastAPI
from app.api.health import router as health_Router
from app.api.auth import router as auth_router
from app.api.user import router as users_router
from app.api.expenses import router as expenses_router

from app.db.database import engine
from app.db.base import Base
from app.models.user import User
from app.models.expense import Expense

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(health_Router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(expenses_router)
