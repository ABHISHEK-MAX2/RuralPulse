from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.domain import MMUOperation, MMUMission, LGDVillage, User
from app.models.schemas import MMUResponse, MMUMissionResponse, MMUMissionCreateRequest
from app.routers.auth import get_current_user
from app.services.audit_service import AuditLogger

router = APIRouter(prefix="/mmus", tags=["MMU Fleet & Missions"])

@router.get("", response_model=List[MMUResponse])
def get_mmu_fleet(district_code: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(MMUOperation)
    if district_code:
        query = query.filter(MMUOperation.district_code == district_code)
    results = query.all()
    return [
        MMUResponse(
            id=m.id,
            mmu_id=m.mmu_id,
            mmu_name=m.mmu_name,
            district_code=m.district_code,
            taluk_code=m.taluk_code,
            status=m.status,
            assigned_area=m.assigned_area,
            available_from=m.available_from,
            data_status=m.data_status or "NOT PUBLICLY AVAILABLE — REQUIRES AUTHORIZED OPERATIONAL SYSTEM ACCESS"
        )
        for m in results
    ]

@router.get("/missions", response_model=List[MMUMissionResponse])
def get_mmu_missions(district_code: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(MMUMission, LGDVillage).join(LGDVillage, MMUMission.village_code == LGDVillage.village_code)
    if district_code:
        query = query.filter(LGDVillage.district_code == district_code)
        
    results = query.order_by(MMUMission.id.desc()).all()
    return [
        MMUMissionResponse(
            id=m.id,
            mmu_id=m.mmu_id,
            village_code=m.village_code,
            village_name=v.village_name,
            mission_name=m.mission_name,
            scheduled_date=m.scheduled_date,
            status=m.status,
            priority=m.priority,
            beneficiaries_targeted=m.beneficiaries_targeted,
            beneficiaries_served=m.beneficiaries_served,
            clinical_notes=m.clinical_notes,
            assigned_by=m.assigned_by,
            created_at=m.created_at,
            completed_at=m.completed_at
        )
        for m, v in results
    ]

from app.services.intervention_engine import apply_intervention_vulnerability_reduction

@router.post("/dispatch", response_model=MMUMissionResponse)
def dispatch_mmu(
    mission_req: MMUMissionCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    v = db.query(LGDVillage).filter(LGDVillage.village_code == mission_req.village_code).first()
    if not v:
        raise HTTPException(status_code=404, detail="Village not found")

    mission = MMUMission(
        mmu_id=mission_req.mmu_id,
        village_code=mission_req.village_code,
        mission_name=mission_req.mission_name,
        scheduled_date=mission_req.scheduled_date,
        status="ASSIGNED",
        priority=mission_req.priority,
        beneficiaries_targeted=mission_req.beneficiaries_targeted,
        assigned_by=current_user.full_name
    )
    db.add(mission)
    db.commit()
    db.refresh(mission)

    # Closed-loop vulnerability reduction for MMU dispatch
    apply_intervention_vulnerability_reduction(
        db=db,
        village_code=mission_req.village_code,
        reduction_amount=25.0,
        reason=f"MMU Fleet Dispatched: {mission_req.mission_name}",
        user_email=current_user.email,
        user_role=current_user.role
    )

    # Log action to audit
    AuditLogger.log_action(
        db=db,
        user_id=current_user.email,
        user_role=current_user.role,
        action="MMU_MISSION_DISPATCH",
        resource=f"MMU_{mission_req.mmu_id}",
        details={
            "village_code": mission_req.village_code,
            "scheduled_date": mission_req.scheduled_date
        }
    )

    return MMUMissionResponse(
        id=mission.id,
        mmu_id=mission.mmu_id,
        village_code=mission.village_code,
        village_name=v.village_name,
        mission_name=mission.mission_name,
        scheduled_date=mission.scheduled_date,
        status=mission.status,
        priority=mission.priority,
        beneficiaries_targeted=mission.beneficiaries_targeted,
        beneficiaries_served=mission.beneficiaries_served,
        clinical_notes=mission.clinical_notes,
        assigned_by=mission.assigned_by,
        created_at=mission.created_at,
        completed_at=mission.completed_at
    )
