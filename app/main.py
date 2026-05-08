from fastapi import FastAPI
from app.api.health import router as health_Router
from app.db.database import engine
from app.db.base import Base
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(health_Router)

