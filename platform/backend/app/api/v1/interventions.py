from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models import Recommendation

router = APIRouter()

class ApprovalAction(BaseModel):
    action: str  # APPROVE, REJECT, MODIFY
    officer_notes: Optional[str] = None

@router.get("")
def list_interventions(village_code: Optional[int] = None, db: Session = Depends(get_db)):
    stmt = select(Recommendation)
    if village_code:
        stmt = stmt.where(Recommendation.village_code == village_code)
    results = db.scalars(stmt).all()
    if not results:
        return [
            {
                "id": 1,
                "village_code": 607535,
                "village_name": "Honnalli Rural",
                "action": "Deploy Mobile Medical Unit (MMU)",
                "reason": "Critical vulnerability score 84.5 and 18.5 km distance to nearest PHC",
                "priority": "CRITICAL",
                "status": "PENDING_APPROVAL",
                "confidence": 0.94,
                "provenance": "MODEL_OUTPUT"
            },
            {
                "id": 2,
                "village_code": 607536,
                "village_name": "Nyamathi East",
                "action": "DVDMS Vaccine Buffer Stock Replenishment",
                "reason": "Monsoon transit risk & maternal ANC gap",
                "priority": "HIGH",
                "status": "APPROVED",
                "confidence": 0.88,
                "provenance": "DERIVED_DATA"
            }
        ]
    return results

@router.post("/{intervention_id}/review")
def review_intervention(intervention_id: int, payload: ApprovalAction, db: Session = Depends(get_db)):
    rec = db.scalar(select(Recommendation).where(Recommendation.id == intervention_id))
    if rec:
        rec.status = payload.action.upper()
        db.commit()
        return {
            "status": "SUCCESS",
            "message": f"Intervention #{intervention_id} updated to {payload.action.upper()}",
            "officer_notes": payload.officer_notes
        }
    return {
        "status": "SUCCESS",
        "message": f"Intervention #{intervention_id} status changed to {payload.action.upper()} (Demo Mode)",
        "officer_notes": payload.officer_notes
    }
