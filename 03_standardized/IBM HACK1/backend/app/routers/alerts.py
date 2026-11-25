from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.domain import Alert, LGDVillage, User
from app.models.schemas import AlertResponse, AlertActionRequest
from app.routers.auth import get_current_user
from app.services.audit_service import AuditLogger

router = APIRouter(prefix="/alerts", tags=["Intelligent Alerts"])

@router.get("", response_model=List[AlertResponse])
def get_alerts(
    district_code: Optional[int] = None,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Alert, LGDVillage).outerjoin(LGDVillage, Alert.village_code == LGDVillage.village_code)
    if district_code:
        query = query.filter(Alert.district_code == district_code)
    if status:
        query = query.filter(Alert.status == status.upper())
    if severity:
        query = query.filter(Alert.severity == severity.upper())

    results = query.order_by(Alert.id.desc()).limit(limit).all()

    return [
        AlertResponse(
            id=a.id,
            village_code=a.village_code,
            village_name=v.village_name if v else None,
            district_code=a.district_code,
            district_name=v.district_name if v else "Karnataka District",
            alert_type=a.alert_type,
            title=a.title,
            description=a.description,
            severity=a.severity,
            status=a.status,
            assigned_to=a.assigned_to,
            recommended_action=a.recommended_action,
            created_at=a.created_at
        )
        for a, v in results
    ]

from app.services.intervention_engine import apply_intervention_vulnerability_reduction

@router.post("/{id}/action", response_model=AlertResponse)
def handle_alert_action(
    id: int,
    action_req: AlertActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(Alert.id == id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    act = action_req.action.upper()
    if act == "ACKNOWLEDGE":
        alert.status = "ACKNOWLEDGED"
        alert.acknowledged_at = datetime.utcnow()
    elif act == "ASSIGN":
        alert.status = "ASSIGNED"
        alert.assigned_to = action_req.assigned_to or current_user.full_name
    elif act == "RESOLVE":
        alert.status = "RESOLVED"
        alert.resolved_at = datetime.utcnow()
        if alert.village_code:
            apply_intervention_vulnerability_reduction(
                db=db,
                village_code=alert.village_code,
                reduction_amount=15.0,
                reason=f"Alert Resolved: {alert.title}",
                user_email=current_user.email,
                user_role=current_user.role
            )
    elif act == "ESCALATE":
        alert.status = "ESCALATED"
        alert.severity = "CRITICAL"

    db.commit()
    db.refresh(alert)

    AuditLogger.log_action(
        db=db,
        user_id=current_user.email,
        user_role=current_user.role,
        action=f"ALERT_{act}",
        resource=f"ALERT_{alert.id}",
        details={"status": alert.status, "assigned_to": alert.assigned_to}
    )

    v = db.query(LGDVillage).filter(LGDVillage.village_code == alert.village_code).first() if alert.village_code else None

    return AlertResponse(
        id=alert.id,
        village_code=alert.village_code,
        village_name=v.village_name if v else None,
        district_code=alert.district_code,
        district_name=v.district_name if v else None,
        alert_type=alert.alert_type,
        title=alert.title,
        description=alert.description,
        severity=alert.severity,
        status=alert.status,
        assigned_to=alert.assigned_to,
        recommended_action=alert.recommended_action,
        created_at=alert.created_at
    )

from app.services.weather_sync import sync_live_open_meteo_weather

@router.post("/sync-live-weather", tags=["Intelligent Alerts"])
def trigger_live_weather_sync(db: Session = Depends(get_db)):
    """
    Triggers live Open-Meteo weather API sync across all Karnataka districts.
    """
    return sync_live_open_meteo_weather(db)

