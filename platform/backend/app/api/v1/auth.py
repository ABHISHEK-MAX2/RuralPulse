from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.rbac import NAV_BY_ROLE
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models import User

router = APIRouter()


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    district_code: int | None
    locale: str
    navigation: list[str]
    demo_mode: bool = True


@router.post("/login", response_model=TokenOut)
@router.post("/token", response_model=TokenOut)
def login(
    request: Request,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.scalar(select(User).where(User.email == form.username))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled")
    token = create_access_token(user.email, extra={"role": user.role, "uid": user.id})
    return TokenOut(access_token=token)


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}
