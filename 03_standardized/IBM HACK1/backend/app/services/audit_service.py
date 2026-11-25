import hashlib
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.domain import AuditLog

class AuditLogger:
    """
    Tamper-resistant audit logging service with SHA-256 hash chaining.
    """
    
    @staticmethod
    def log_action(
        db: Session,
        user_id: str,
        user_role: str,
        action: str,
        resource: str,
        details: dict
    ) -> AuditLog:
        # Fetch latest audit log record to get previous hash
        last_log = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
        prev_hash = last_log.log_hash if last_log else "GENESIS_BLOCK_0000000000000000"
        
        timestamp_str = datetime.utcnow().isoformat()
        details_str = json.dumps(details, sort_keys=True)
        
        raw_payload = f"{timestamp_str}|{user_id}|{user_role}|{action}|{resource}|{details_str}|{prev_hash}"
        log_hash = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()
        
        log_entry = AuditLog(
            user_id=str(user_id),
            user_role=user_role,
            action=action,
            resource=resource,
            details_json=details_str,
            prev_hash=prev_hash,
            log_hash=log_hash,
            timestamp=datetime.utcnow()
        )
        
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry
