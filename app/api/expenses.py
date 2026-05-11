from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from fastapi import HTTPException

from typing import Optional
from datetime import datetime
from fastapi import Query

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
    category: Optional[str]= None,
    start_date: Optional[datetime]= None,
    end_date: Optional[datetime]= None,
    skip: int = Query(0,ge=0),
    limit: int = Query(10,ge=1, le=100),
    sort_order: str = Query("desc"),
    db:Session =Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Expense).filter(
        Expense.owner_id == current_user.id
    )
    if category:
        query = query.filter(
            Expense.category.ilike(category)
        )

    if start_date:
        query = query.filter(
            Expense.created_at >= start_date
        )

    if end_date:
        query = query.filter(
            Expense.created_at <= end_date
        )

    if sort_order == "asc":
        query = query.order_by(
            Expense.created_at.asc()
        )
    else:
        query = query.order_by(
            Expense.created_at.desc()
        )

    expenses = query.offset(skip).limit(limit).all()
  

    return expenses

@router.put("/{expense_id}",response_model=ExpenseResponse)
def update_expense(expense_id:int, updated_data:ExpenseUpdate, db:Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.owner_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code = 404,
            detail="Expense not found"
        )
        
    expense.title = updated_data.title
    expense.amount = updated_data.amount
    expense.category = updated_data.category
    
    db.commit()
    db.refresh(expense)
    
    return expense


@router.delete("/{expense_id}",status_code=200)
def delete_expense(
    expense_id:int,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.owner_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
        
    db.delete(expense)
    db.commit()
    
    return{
        "message":"Expense deleted sussessfully"
    }