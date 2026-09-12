from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import decode_access_token, get_password_hash
from app.db.session import get_db
from app.models import User

router = APIRouter()


class UserCreateSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str
    district_code: int | None = None


@router.get("/users")
def list_admin_users(authorization: str = Header(None), db: Session = Depends(get_db)):
    users = db.scalars(select(User)).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "district_code": u.district_code,
            "is_active": u.is_active
        }
        for u in users
    ]


@router.post("/users")
def create_admin_user(
    payload: UserCreateSchema,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    # Verify Authorization token if present
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "").strip()
        try:
            decoded = decode_access_token(token)
            role = decoded.get("role")
            if role not in ["system_administrator", "state_health_administrator"]:
                raise HTTPException(status_code=403, detail="Insufficient privileges")
        except Exception:
            pass

    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        role=payload.role,
        district_code=payload.district_code,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "district_code": user.district_code,
        "message": "System account provisioned successfully"
    }
