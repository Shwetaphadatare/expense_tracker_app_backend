from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("/", response_model=ExpenseResponse,status_code=status.HTTP_201_CREATED)
def create_expense(expense:ExpenseCreate, db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    new_expense = Expense(
        title =expense.title,
        amount=expense.amount,
        category=expense.category,
        owner_id=current_user.id
        
    )
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    return new_expense


@router.get("/",response_model=list[ExpenseResponse])
def get_my_expenses(
    db:Session =Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expenses = db.query(Expense).filter(
        Expense.owner_id == current_user.id
    ).all()
    
    return expenses