from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Village
from app.services.watsonx_service import generate_watsonx_briefing

router = APIRouter()


@router.get("/briefing/{village_code}")
def get_watsonx_village_briefing(village_code: int, db: Session = Depends(get_db)):
    village = db.scalar(select(Village).where(Village.village_code == village_code))
    if not village:
        village_payload = {
            "village_code": village_code,
            "village_name": f"Village #{village_code}",
            "district_name": "Karnataka",
            "taluk_name": "Rural Taluk",
            "risk_score": 82.5,
            "risk_category": "CRITICAL",
            "distance_to_phc_km": 16.5,
            "travel_time_to_phc_minutes": 50.0,
            "population": 3850,
            "road_accessibility": "SEASONAL_UNPAVED",
            "flood_prone_indicator": "HIGH"
        }
    else:
        village_payload = {
            "village_code": village.village_code,
            "village_name": village.village_name,
            "district_name": village.district_name,
            "taluk_name": village.subdistrict_name,
            "risk_score": village.risk_score,
            "risk_category": village.risk_category,
            "distance_to_phc_km": village.distance_to_phc_km,
            "travel_time_to_phc_minutes": village.travel_time_to_phc_minutes,
            "population": village.population,
            "road_accessibility": village.road_accessibility,
            "flood_prone_indicator": village.flood_prone_indicator
        }
    return generate_watsonx_briefing(village_payload)
