from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user

from app.models.recurring_expense import RecurringExpense
from app.models.expense import Expense
from app.models.user import User

from app.schemas.recurring_expense import(
    RecurringExpenseCreate,
    RecurringExpenseResponse
)

router = APIRouter(
    prefix="/recurring-expenses",
    tags=["Recurring Expenses"]
)



@router.post("/",response_model=RecurringExpenseResponse,
             status_code=status.HTTP_201_CREATED)

def create_recurring_expense(
    recurring: RecurringExpenseCreate,
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    if recurring.frequency not in ["monthly","weekly"]:
        raise HTTPException(
            status_code=400,
            detail="Frequency must be monthly or weekly"
        )
        
    new_recurring = RecurringExpense(
        title=recurring.title,
        amount=recurring.amount,
        category=recurring.category,
        frequency=recurring.frequency,
        next_due_date=recurring.next_due_date,
        owner_id=current_user.id
    )
    
    db.add(new_recurring)
    db.commit()
    db.refresh(new_recurring)
    
    return new_recurring


@router.get("/",response_model=list[RecurringExpenseResponse])
def get_recurring_expenses(
    db:Session=Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    return db.query(RecurringExpense).filter(
        RecurringExpense.owner_id == current_user.id
    ).all()
    
    
@router.post("/process")
def process_recurring_expense(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recurring_expenses = db.query(
        RecurringExpense
    ).filter(
        RecurringExpense.owner_id == current_user.id,
        RecurringExpense.next_due_date <= datetime.now()
    ).all()
    
    processed_count = 0
    
    for recurring in recurring_expenses:
        new_expense = Expense(
            title=recurring.title,
            amount = recurring.amount,
            category = recurring.category,
            owner_id=current_user.id
        )
        
        db.add(new_expense)
    
        if recurring.frequency == "monthly":
            recurring.next_due_date += timedelta(days=30)
        elif recurring.frequency =="weekly":
            recurring.next_due_date += timedelta(days=7)
        
        processed_count += 1
    
    db.commit()
    
    return{
        "message":f"{processed_count} recurring expenses processed successfully"
    }
      