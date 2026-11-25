from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.models.domain import (
    LGDVillage, VulnerabilityScore, MMUMission, AIRecommendation, User
)
from app.routers.auth import get_current_user
from app.services.audit_service import AuditLogger

router = APIRouter(prefix="/reports", tags=["Executive Reports"])

class ReportRequest(BaseModel):
    report_type: str  # DISTRICT_HEALTH_REPORT, HIGH_RISK_REGISTER, MMU_MISSION_LOG
    district_code: Optional[int] = 524
    format: str = "PDF"  # PDF, EXCEL, CSV

@router.post("/generate")
def generate_report(
    req: ReportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    AuditLogger.log_action(
        db=db,
        user_id=current_user.email,
        user_role=current_user.role,
        action="REPORT_GENERATION",
        resource=req.report_type,
        details={"district_code": req.district_code, "format": req.format}
    )

    query = (
        db.query(LGDVillage, VulnerabilityScore)
        .join(VulnerabilityScore, LGDVillage.village_code == VulnerabilityScore.village_code)
    )
    if req.district_code:
        query = query.filter(LGDVillage.district_code == req.district_code)

    top_villages = query.order_by(VulnerabilityScore.score.desc()).limit(50).all()

    fmt = req.format.upper()
    if fmt in ("CSV", "EXCEL"):
        csv_lines = [
            "Village Code,Village Name,District Name,Taluk Name,Vulnerability Score,Risk Level,7-Day Forecast Score,Healthcare Access Subscore,Maternal Care Subscore"
        ]
        for v, s in top_villages:
            v_name = f'"{v.village_name}"' if ',' in v.village_name else v.village_name
            t_name = f'"{v.taluk_name}"' if ',' in v.taluk_name else v.taluk_name
            d_name = f'"{v.district_name}"' if ',' in v.district_name else v.district_name
            csv_lines.append(f"{v.village_code},{v_name},{d_name},{t_name},{s.score},{s.risk_level},{s.predicted_score_7d},{s.healthcare_access_subscore},{s.maternal_child_subscore}")
        report_text = "\n".join(csv_lines)
    else:
        report_content = []
        report_content.append(f"KARNATAKA RURAL HEALTHCARE INTELLIGENCE & DECISION SUPPORT PLATFORM")
        report_content.append(f"OFFICIAL HEALTH ADMINISTRATION REPORT: {req.report_type}")
        report_content.append(f"Generated On: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report_content.append(f"Requesting Official: {current_user.full_name} ({current_user.role})")
        report_content.append(f"District Filter: Code {req.district_code}")
        report_content.append("=" * 75)
        report_content.append("\nHIGH RISK VILLAGES REQUIRING IMMEDIATE INTERVENTION:")
        report_content.append("-" * 75)

        for v, s in top_villages:
            report_content.append(f"• Village: {v.village_name} (Code: {v.village_code}) | Taluk: {v.taluk_name}")
            report_content.append(f"  Vulnerability Score: {s.score}/100 [{s.risk_level}] | 7-Day Forecast: {s.predicted_score_7d}")
            report_content.append(f"  Healthcare Access Subscore: {s.healthcare_access_subscore} | Maternal Care: {s.maternal_child_subscore}")
            report_content.append("")

        report_text = "\n".join(report_content)

    return {
        "report_id": f"REP-KAR-{req.district_code}-{int(datetime.utcnow().timestamp())}",
        "report_type": req.report_type,
        "format": req.format,
        "generated_by": current_user.full_name,
        "generated_at": datetime.utcnow().isoformat(),
        "summary": f"Official {req.format} report generated successfully containing {len(top_villages)} vulnerability profiles.",
        "content_text": report_text,
        "download_url": f"/api/v1/reports/download/sample.{req.format.lower()}"
    }
