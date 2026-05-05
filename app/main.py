from fastapi import FastAPI
from app.api.health import router as health_Router

app = FastAPI(title="Expense Tracker API")

app.include_router(health_Router)

