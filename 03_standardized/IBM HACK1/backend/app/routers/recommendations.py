from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.domain import AIRecommendation, LGDVillage, User
from app.models.schemas import RecommendationResponse, RecommendationReviewRequest
from app.routers.auth import get_current_user
from app.services.audit_service import AuditLogger

router = APIRouter(prefix="/recommendations", tags=["Human-in-the-Loop Recommendations"])

@router.get("", response_model=List[RecommendationResponse])
def get_recommendations(
    district_code: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(AIRecommendation, LGDVillage).join(LGDVillage, AIRecommendation.village_code == LGDVillage.village_code)
    
    if district_code:
        query = query.filter(LGDVillage.district_code == district_code)
    if status:
        query = query.filter(AIRecommendation.status == status.upper())

    results = query.order_by(AIRecommendation.id.desc()).limit(limit).all()

    return [
        RecommendationResponse(
            id=rec.id,
            village_code=rec.village_code,
            village_name=v.village_name,
            district_code=v.district_code,
            action=rec.action,
            reason=rec.reason,
            priority=rec.priority,
            expected_impact=rec.expected_impact,
            required_resources=rec.required_resources,
            suggested_deadline=rec.suggested_deadline,
            confidence=rec.confidence,
            status=rec.status,
            approved_by=rec.approved_by,
            approved_at=rec.approved_at,
            rejection_reason=rec.rejection_reason
        )
        for rec, v in results
    ]

from app.services.intervention_engine import apply_intervention_vulnerability_reduction

@router.post("/{id}/review", response_model=RecommendationResponse)
def review_recommendation(
    id: int,
    review_req: RecommendationReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rec = db.query(AIRecommendation).filter(AIRecommendation.id == id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    rec.status = review_req.status.upper()
    rec.approved_by = current_user.full_name
    rec.approved_at = datetime.utcnow()
    if review_req.notes:
        rec.rejection_reason = review_req.notes

    db.commit()
    db.refresh(rec)

    # Closed-loop severity reduction if approved
    if rec.status == "APPROVED":
        apply_intervention_vulnerability_reduction(
            db=db,
            village_code=rec.village_code,
            reduction_amount=20.0,
            reason=f"AI Recommendation Approved: {rec.action}",
            user_email=current_user.email,
            user_role=current_user.role
        )

    # Log to audit trail
    AuditLogger.log_action(
        db=db,
        user_id=current_user.email,
        user_role=current_user.role,
        action=f"RECOMMENDATION_{rec.status}",
        resource=f"AI_RECOMMENDATION_{rec.id}",
        details={
            "village_code": rec.village_code,
            "action": rec.action,
            "notes": review_req.notes
        }
    )

    v = db.query(LGDVillage).filter(LGDVillage.village_code == rec.village_code).first()

    return RecommendationResponse(
        id=rec.id,
        village_code=rec.village_code,
        village_name=v.village_name if v else None,
        district_code=v.district_code if v else None,
        action=rec.action,
        reason=rec.reason,
        priority=rec.priority,
        expected_impact=rec.expected_impact,
        required_resources=rec.required_resources,
        suggested_deadline=rec.suggested_deadline,
        confidence=rec.confidence,
        status=rec.status,
        approved_by=rec.approved_by,
        approved_at=rec.approved_at,
        rejection_reason=rec.rejection_reason
    )
