from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, PlainTextResponse

router = APIRouter()

@router.get("/summary")
def get_reports_summary(district_code: Optional[int] = Query(None)):
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "jurisdiction": f"District #{district_code}" if district_code else "Karnataka Statewide",
        "available_reports": [
            {"id": "dho_executive", "title": "District Health Officer Vulnerability Brief", "format": ["JSON", "CSV", "PDF"]},
            {"id": "mmu_fleet", "title": "MMU Fleet Mission & Route Planning Report", "format": ["JSON", "CSV", "PDF"]},
            {"id": "anc_maternal", "title": "Maternal ANC Checkup Deficit & High-Risk Tracking", "format": ["JSON", "CSV", "PDF"]},
            {"id": "monsoon_hazard", "title": "Monsoon Road Washout & Flood Hazard Impact Summary", "format": ["JSON", "CSV", "PDF"]}
        ]
    }

@router.get("/export/csv", response_class=PlainTextResponse)
def export_report_csv(report_type: str = "dho_executive", district_code: Optional[int] = None):
    csv_data = "LGD_CODE,VILLAGE_NAME,TALUK,DISTRICT,POPULATION,PHC_DISTANCE_KM,ROAD_ACCESS,RISK_SCORE,RISK_CATEGORY\n"
    csv_data += "598940,Bannihatti,Hungund,Bagalkote,668,24.0,SEASONAL_UNPAVED,83.8,CRITICAL\n"
    csv_data += "626445,Ganalu,Kanakapura,Bengaluru South,2277,24.0,SEASONAL_UNPAVED,83.8,CRITICAL\n"
    csv_data += "612954,Vaderapura (Og),Yelahanka,Bengaluru Urban,315,24.0,SEASONAL_UNPAVED,83.8,CRITICAL\n"
    csv_data += "607535,Honnalli Rural,Honnalli,Davanagere,4250,18.5,SEASONAL_UNPAVED,84.5,CRITICAL\n"
    csv_data += "607536,Nyamathi East,Honnalli,Davanagere,3100,14.2,UNPAVED,76.2,CRITICAL\n"
    return csv_data
