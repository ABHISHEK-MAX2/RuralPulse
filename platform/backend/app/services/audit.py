"""Audit Logging Service for RBAC actions."""
from sqlalchemy.orm import Session
from app.models import AuditLog, User


def write_audit(
    db: Session,
    action: str,
    resource: str,
    user: User | None = None,
    ip: str | None = None,
    user_agent: str | None = None
):
    try:
        log = AuditLog(
            user_email=user.email if user else "anonymous",
            user_role=user.role if user else "guest",
            action=action,
            resource=resource,
            ip_address=ip,
            user_agent=user_agent
        )
        db.add(log)
    except Exception:
        pass
