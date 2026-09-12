from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models import User


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.replace("Bearer ", "").strip()
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email:
            return None
        user = db.scalar(select(User).where(User.email == email))
        return user
    except Exception:
        return None
