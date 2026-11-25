from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.domain import AuditLog

router = APIRouter(prefix="/audit", tags=["Tamper-Resistant Audit Log"])

@router.get("/logs")
def get_audit_logs(limit: int = Query(50, le=200), db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(limit).all()
    return [
        {
            "id": log.id,
            "timestamp": log.timestamp.isoformat(),
            "user_id": log.user_id,
            "user_role": log.user_role,
            "action": log.action,
            "resource": log.resource,
            "details": log.details_json,
            "prev_hash": log.prev_hash,
            "log_hash": log.log_hash
        }
        for log in logs
    ]
