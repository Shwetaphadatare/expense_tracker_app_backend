from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.expense import Expense
from app.models.user import User
from app.schemas.dashboard import(
    DashboardSummary,
    CategoryBreakdown,
    MonthlyBreakdown
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/summary",response_model=DashboardSummary)
def get_dashboard_summary(
    db:Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    total,count = db.query(
        func.coalesce(func.sum(Expense.amount), 0),
        func.count(Expense.id)
    ).filter(
        Expense.owner_id == current_user.id
    ).first()
    
    return{
        "total_expenses":total,
        "total_transactions":count
    }
    

@router.get("/category-breakdown",response_model=list[CategoryBreakdown])
def get_category_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        Expense.category,
        func.sum(Expense.amount).label("total_amount")
    ).filter(
        Expense.owner_id == current_user.id
    ).group_by(
        Expense.category
    ).all()
    
    
    return results


@router.get(
    "/monthly-summary",
    response_model=list[MonthlyBreakdown]
)
def get_monthly_summary(
    db:Session=Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        func.to_char(
            Expense.created_at,
            "YYYY-MM"
        ).label("month"),
        func.sum(Expense.amount).label("total_amount")
    ).filter(
        Expense.owner_id == current_user.id
    ).group_by(
        "month"
    ).order_by("month").all()
    
    return results