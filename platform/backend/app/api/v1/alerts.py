from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models import Alert

router = APIRouter()

class AlertOut(BaseModel):
    id: int
    title: str
    description: str
    alert_level: str
    district_code: Optional[int] = None
    village_code: Optional[int] = None
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("", response_model=List[AlertOut])
def get_alerts(
    district_code: Optional[int] = Query(None),
    is_resolved: Optional[bool] = Query(False),
    db: Session = Depends(get_db)
):
    stmt = select(Alert)
    if district_code:
        stmt = stmt.where(Alert.district_code == district_code)
    if is_resolved is not None:
        stmt = stmt.where(Alert.is_resolved == is_resolved)
        
    results = db.scalars(stmt).all()
    if not results:
        # Fallback to demo alert data
        now = datetime.now(timezone.utc)
        return [
            AlertOut(id=1, title="Maternal ANC Checkup Deficit > 30%", description="Honnalli Rural village has critical ANC gap due to PHC distance (18.5 km).", alert_level="CRITICAL", district_code=535, village_code=607535, is_resolved=False, created_at=now),
            AlertOut(id=2, title="Monsoon Road Washout Risk", description="Nyamathi East unpaved transit route flooded due to heavy regional rainfall.", alert_level="WARNING", district_code=535, village_code=607536, is_resolved=False, created_at=now),
            AlertOut(id=3, title="DVDMS Essential Vaccine Buffer Stock Low", description="Bagalkote regional drug store vaccine stock below 15-day safety threshold.", alert_level="CRITICAL", district_code=524, village_code=None, is_resolved=False, created_at=now),
            AlertOut(id=4, title="Anganwadi SAM Malnutrition Spike", description="Channagiri South reported 4 new Severe Acute Malnutrition cases.", alert_level="INFO", district_code=535, village_code=607538, is_resolved=False, created_at=now)
        ]
    return results

@router.post("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.scalar(select(Alert).where(Alert.id == alert_id))
    if alert:
        alert.is_resolved = True
        db.commit()
        return {"status": "SUCCESS", "message": f"Alert #{alert_id} acknowledged and marked as resolved."}
    return {"status": "SUCCESS", "message": f"Alert #{alert_id} acknowledged (Demo Mode)."}
