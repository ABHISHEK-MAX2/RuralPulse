from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.domain import HealthFacility

router = APIRouter(prefix="/facilities", tags=["Health Facilities"])

@router.get("")
def get_facilities(
    district_code: Optional[int] = None,
    taluk_code: Optional[int] = None,
    facility_type: Optional[str] = None,
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    query = db.query(HealthFacility)
    if district_code:
        query = query.filter(HealthFacility.district_code == district_code)
    if taluk_code:
        query = query.filter(HealthFacility.taluk_code == taluk_code)
    if facility_type:
        query = query.filter(HealthFacility.facility_type == facility_type.upper())
        
    results = query.limit(limit).all()
    return [
        {
            "facility_id": f.facility_id,
            "facility_name": f.facility_name,
            "facility_type": f.facility_type,
            "sub_centre_or_phc_or_chc": f.sub_centre_or_phc_or_chc,
            "district_code": f.district_code,
            "taluk_code": f.taluk_code,
            "latitude": f.latitude,
            "longitude": f.longitude,
            "beds": f.beds,
            "doctors_sanctioned": f.doctors_sanctioned,
            "doctors_in_position": f.doctors_in_position,
            "nurses_sanctioned": f.nurses_sanctioned,
            "nurses_in_position": f.nurses_in_position,
            "anm_available": f.anm_available,
            "facility_status": f.facility_status
        }
        for f in results
    ]
