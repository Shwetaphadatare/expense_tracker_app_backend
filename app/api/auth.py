from fastapi import APIRouter, Cookie, Depends, HTTPException, status,Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.database import SessionLocal
from app.dependencies.db import get_db
from app.models.user import User
from app.models.session import Session as SessionModel
from app.schemas.user import userCreate, UserResponse,UserLogin,Token
from app.core.security import hash_password,verify_password,create_access_token, create_refresh_token
from app.services.session_service import create_session, delete_session, get_session

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(user:userCreate, db:Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
        
    secure_password = hash_password(user.password)
    
    new_user = User(
        full_name = user.full_name,
        email=user.email,
        hashed_password=secure_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post(
    "/login",
    response_model=Token
)
def login_user(user:UserLogin,response:Response,db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()
    
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
        
    if not verify_password(
        user.password,existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
        
    access_token = create_access_token(
        data={"sub":existing_user.email}
    )
    
    refresh_token = create_refresh_token({"sub": existing_user.email})

    expires_at = datetime.now() + timedelta(days=7)

    # store refresh token in DB
    create_session(db, existing_user.id, refresh_token, expires_at)

    # set cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # set True in production HTTPS
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )

    return{
        "access_token":access_token,
        "token_type":"bearer"
    }
    
    
    

@router.post("/refresh")
def refresh_token(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str = Cookie(None)
):

    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    session = get_session(db, refresh_token)

    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    if session.expires_at < datetime.now():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # get user
    user = db.query(User).filter(User.id == session.user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # FIX: consistent identity (EMAIL)
    new_access_token = create_access_token(
        {"sub": user.email}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
    

@router.post("/logout")
def logout(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str = Cookie(None)
):

    if refresh_token:
        delete_session(db, refresh_token)

    response.delete_cookie("refresh_token")

    return {"message": "Logged out successfully"}