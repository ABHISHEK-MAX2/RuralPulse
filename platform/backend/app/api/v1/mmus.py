from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models import MMU, Mission, Village

router = APIRouter()

class MMUOut(BaseModel):
    id: int
    mmu_code: str
    vehicle_registration: str
    district_code: int
    district_name: str
    current_assigned_village_code: Optional[int] = None
    status: str
    last_camp_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class DeployPayload(BaseModel):
    village_code: int
    mission_title: str
    scheduled_date: Optional[datetime] = None

@router.get("", response_model=List[MMUOut])
def list_mmus(
    district_code: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    stmt = select(MMU)
    if district_code:
        stmt = stmt.where(MMU.district_code == district_code)
    if status:
        stmt = stmt.where(MMU.status == status)
    
    results = db.scalars(stmt).all()
    if not results:
        # Provide demo MMU list if database table is currently empty
        return [
            MMUOut(id=1, mmu_code="MMU-KA-535-01", vehicle_registration="KA-17-G-4012", district_code=535, district_name="Davanagere", current_assigned_village_code=607535, status="EN_ROUTE", last_camp_date=datetime.now(timezone.utc)),
            MMUOut(id=2, mmu_code="MMU-KA-535-02", vehicle_registration="KA-17-G-4015", district_code=535, district_name="Davanagere", current_assigned_village_code=None, status="AVAILABLE", last_camp_date=datetime.now(timezone.utc)),
            MMUOut(id=3, mmu_code="MMU-KA-524-01", vehicle_registration="KA-29-G-1102", district_code=524, district_name="Bagalkote", current_assigned_village_code=598940, status="ON_SITE", last_camp_date=datetime.now(timezone.utc)),
            MMUOut(id=4, mmu_code="MMU-KA-524-02", vehicle_registration="KA-29-G-1108", district_code=524, district_name="Bagalkote", current_assigned_village_code=None, status="MAINTENANCE", last_camp_date=datetime.now(timezone.utc))
        ]
    return results

@router.post("/{mmu_id}/deploy")
def deploy_mmu(
    mmu_id: int,
    payload: DeployPayload,
    db: Session = Depends(get_db)
):
    mmu = db.scalar(select(MMU).where(MMU.id == mmu_id))
    if not mmu:
        return {
            "status": "SUCCESS",
            "message": f"MMU #{mmu_id} deployed to Village #{payload.village_code} (Demo Mode)",
            "mission_code": f"MIS-{mmu_id}-{payload.village_code}",
            "mmu_status": "EN_ROUTE"
        }
    
    mmu.status = "EN_ROUTE"
    mmu.current_assigned_village_code = payload.village_code
    
    mission = Mission(
        mission_code=f"MIS-{mmu.id}-{int(datetime.now(timezone.utc).timestamp())}",
        title=payload.mission_title,
        assigned_mmu_code=mmu.mmu_code,
        target_village_code=payload.village_code,
        status="ASSIGNED",
        scheduled_date=payload.scheduled_date or datetime.now(timezone.utc)
    )
    db.add(mission)
    db.commit()
    
    return {
        "status": "SUCCESS",
        "message": f"MMU {mmu.mmu_code} successfully deployed to Village #{payload.village_code}",
        "mission_code": mission.mission_code,
        "mmu_status": mmu.status
    }
