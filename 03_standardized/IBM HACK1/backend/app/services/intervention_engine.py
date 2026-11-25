from sqlalchemy.orm import Session
from datetime import datetime
from app.models.domain import VulnerabilityScore, Alert, LGDVillage
from app.services.audit_service import AuditLogger

def apply_intervention_vulnerability_reduction(
    db: Session,
    village_code: int,
    reduction_amount: float = 20.0,
    reason: str = "Intervention Authorized",
    user_email: str = "system",
    user_role: str = "SYSTEM"
):
    vs = db.query(VulnerabilityScore).filter(VulnerabilityScore.village_code == village_code).first()
    if not vs:
        return None

    old_score = vs.score
    new_score = max(15.0, round(vs.score - reduction_amount, 2))
    vs.score = new_score

    # Determine risk level category
    if new_score >= 75.0:
        new_risk = "CRITICAL"
    elif new_score >= 55.0:
        new_risk = "HIGH"
    elif new_score >= 35.0:
        new_risk = "MEDIUM"
    else:
        new_risk = "LOW"

    vs.risk_level = new_risk

    # Auto-resolve OPEN alerts for this village
    open_alerts = db.query(Alert).filter(
        Alert.village_code == village_code,
        Alert.status.in_(["OPEN", "ACKNOWLEDGED", "ASSIGNED"])
    ).all()

    resolved_alert_ids = []
    for alert in open_alerts:
        alert.status = "RESOLVED"
        alert.resolved_at = datetime.utcnow()
        resolved_alert_ids.append(alert.id)

    db.commit()
    db.refresh(vs)

    # Log to audit trail
    AuditLogger.log_action(
        db=db,
        user_id=user_email,
        user_role=user_role,
        action="CLOSED_LOOP_INTERVENTION_APPLIED",
        resource=f"VILLAGE_{village_code}",
        details={
            "old_score": old_score,
            "new_score": new_score,
            "new_risk_level": new_risk,
            "reduction_amount": reduction_amount,
            "reason": reason,
            "resolved_alert_ids": resolved_alert_ids
        }
    )

    return {
        "village_code": village_code,
        "old_score": old_score,
        "new_score": new_score,
        "new_risk_level": new_risk,
        "resolved_alerts_count": len(resolved_alert_ids)
    }
