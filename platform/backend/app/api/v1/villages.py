from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Village

router = APIRouter()


@router.get("")
def list_villages(
    district_code: Optional[int] = None,
    risk_category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = select(Village)
    if district_code:
        query = query.where(Village.district_code == district_code)
    if risk_category:
        query = query.where(Village.risk_category == risk_category)
    if search:
        query = query.where(Village.village_name.ilike(f"%{search}%"))

    # Priority sorting by risk_score descending
    query = query.order_by(Village.risk_score.desc())

    total = db.scalar(select(Village).count()) or 0
    items = db.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }


@router.get("/{village_code}")
def get_village(village_code: int, db: Session = Depends(get_db)):
    village = db.scalar(select(Village).where(Village.village_code == village_code))
    return village
