from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.budget import Budget
from app.models.expense import Expense
from app.models.user import User

from app.schemas.budget import(
    BudgetCreate,
    BudgetResponse,
    BudgetAlert,
    BudgetUpdate
)

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

@router.post("/",response_model=BudgetResponse,status_code=status.HTTP_201_CREATED)
def create_budget(
    budget: BudgetCreate,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_budget = db.query(Budget).filter(
        Budget.owner_id == current_user.id,
        Budget.category == budget.category,
        Budget.month == budget.month
    ).first()
    
    if existing_budget:
        raise HTTPException(
            status_code=400,
            detail="Budget already existes for this category and month"
        )
        
    new_budget = Budget(
        category=budget.category,
        monthly_limit=budget.monthly_limit,
        month=budget.month,
        owner_id=current_user.id
    )
    
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    
    return new_budget


@router.get("/",response_model=list[BudgetResponse])
def get_budgets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Budget).filter(
        Budget.owner_id == current_user.id
    ).all()



@router.put("/{budget_id}",response_model=BudgetResponse)
def update_budget(
    budget_id:int,
    updated_budget:BudgetUpdate,
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    existing_budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.owner_id == current_user.id
    ).first()
    
    if not existing_budget:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )
        
    duplicate_budget = db.query(Budget).filter(
        Budget.owner_id == current_user.id,
        Budget.category == updated_budget.category,
        Budget.month == updated_budget.month,
        Budget.id != budget_id
    ).first()
    
    if duplicate_budget:
        raise HTTPException(
            status_code=400,
            detail="Budget alreay exists for this category and month"
        )
        
    existing_budget.category = updated_budget.category
    existing_budget.monthly_limit = updated_budget.monthly_limit
    existing_budget.month = updated_budget.month
    
    db.commit()
    db.refresh(existing_budget)
    
    return existing_budget

@router.delete("/{budget_id}",status_code=200)
def delete_budget(budget_id:int,
        db:Session = Depends(get_db),
        current_user:User = Depends(get_current_user)):
    
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.owner_id == current_user.id
    ).first()
    
    if not budget:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )
        
    db.delete(budget)
    db.commit()
    
    return{
        "message":"Budget deleted sucessfully"
    }
    


@router.get(
    "/alerts",
    response_model=list[BudgetAlert]
)
def get_budget_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    budgets = db.query(Budget).filter(
        Budget.owner_id == current_user.id
    ).all()

    alerts = []
   
    for budget in budgets:

        spent = db.query(
    func.coalesce(func.sum(Expense.amount), 0)
).filter(
    Expense.owner_id == current_user.id,
    func.lower(func.trim(Expense.category)) ==
    budget.category.value.strip().lower(),
    func.to_char(
    Expense.created_at,
    "YYYY-MM"
    ) == budget.month   
).scalar()

        remaining = budget.monthly_limit - spent

        if spent > budget.monthly_limit:
            status = "Exceeded"
        elif spent == budget.monthly_limit:
            status = "Limit Reached"
        else:
            status = "Within Budget"

        alerts.append({
            "category": budget.category.value,
            "monthly_limit": budget.monthly_limit,
            "spent": spent,
            "remaining": remaining,
            "status": status
        })

    return alerts
