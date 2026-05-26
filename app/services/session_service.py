from sqlalchemy.orm import Session
from datetime import datetime

from app.models.session import Session as SessionModel

def create_session(db: Session, user_id: int, refresh_token: str, expires_at: datetime):

    session_obj = SessionModel(
        user_id=user_id,
        refresh_token=refresh_token,
        expires_at=expires_at
    )

    db.add(session_obj)
    db.commit()
    db.refresh(session_obj)

    return session_obj


def get_session(db: Session, token: str):
    return db.query(SessionModel).filter(
        SessionModel.refresh_token == token
    ).first()


def delete_session(db: Session, token: str):
    db.query(SessionModel).filter(
        SessionModel.refresh_token == token
    ).delete()
    db.commit()