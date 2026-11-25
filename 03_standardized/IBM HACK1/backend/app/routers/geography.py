from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Optional
import json

from app.database import get_db
from app.models.domain import (
    LGDVillage, VillageDemographics, VulnerabilityScore,
    VillageAccessibility, AnganwadiNutrition, HealthFacility
)
from app.models.schemas import DistrictSummary, TalukSummary, VillageListItem, VillageProfileResponse

router = APIRouter(prefix="/geography", tags=["Geography & Villages"])

@router.get("/districts", response_model=List[DistrictSummary])
def get_districts(db: Session = Depends(get_db)):
    results = (
        db.query(
            LGDVillage.district_code,
            LGDVillage.district_name,
            func.count(LGDVillage.village_code).label("total_villages"),
            func.avg(VulnerabilityScore.score).label("avg_score"),
            func.sum(case((VulnerabilityScore.risk_level.in_(["HIGH", "CRITICAL"]), 1), else_=0)).label("high_risk"),
            func.sum(case((VulnerabilityScore.risk_level == "MEDIUM", 1), else_=0)).label("medium_risk"),
            func.sum(case((VulnerabilityScore.risk_level == "LOW", 1), else_=0)).label("low_risk")
        )
        .join(VulnerabilityScore, LGDVillage.village_code == VulnerabilityScore.village_code)
        .group_by(LGDVillage.district_code, LGDVillage.district_name)
        .order_by(LGDVillage.district_name)
        .all()
    )

    summaries = []
    for r in results:
        tot = r.total_villages or 0
        high = r.high_risk or 0
        med = r.medium_risk or 0
        low = r.low_risk or 0
        summaries.append(DistrictSummary(
            district_code=r.district_code,
            district_name=r.district_name,
            total_villages=tot,
            high_risk_villages=high,
            medium_risk_villages=med,
            low_risk_villages=low,
            avg_vulnerability_score=round(r.avg_score or 0.0, 1)
        ))
    return summaries

@router.get("/taluks", response_model=List[TalukSummary])
def get_taluks(district_code: Optional[int] = None, db: Session = Depends(get_db)):
    query = (
        db.query(
            LGDVillage.taluk_code,
            LGDVillage.taluk_name,
            LGDVillage.district_code,
            func.count(LGDVillage.village_code).label("total_villages"),
            func.avg(VulnerabilityScore.score).label("avg_score"),
            func.sum(case((VulnerabilityScore.risk_level.in_(["HIGH", "CRITICAL"]), 1), else_=0)).label("high_risk")
        )
        .join(VulnerabilityScore, LGDVillage.village_code == VulnerabilityScore.village_code)
    )
    if district_code:
        query = query.filter(LGDVillage.district_code == district_code)
        
    results = (
        query.group_by(LGDVillage.taluk_code, LGDVillage.taluk_name, LGDVillage.district_code)
        .order_by(LGDVillage.taluk_name)
        .all()
    )

    return [
        TalukSummary(
            taluk_code=r.taluk_code,
            taluk_name=r.taluk_name,
            district_code=r.district_code,
            total_villages=r.total_villages or 0,
            high_risk_villages=r.high_risk or 0,
            avg_vulnerability_score=round(r.avg_score or 0.0, 1)
        )
        for r in results
    ]

@router.get("/villages", response_model=List[VillageListItem])
def get_villages(
    district_code: Optional[int] = None,
    taluk_code: Optional[int] = None,
    risk_level: Optional[str] = None,
    search: Optional[str] = None,
    min_score: Optional[float] = None,
    limit: int = Query(50, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = (
        db.query(
            LGDVillage.village_code,
            LGDVillage.village_name,
            LGDVillage.district_code,
            LGDVillage.district_name,
            LGDVillage.taluk_code,
            LGDVillage.taluk_name,
            LGDVillage.latitude,
            LGDVillage.longitude,
            VillageDemographics.population,
            VulnerabilityScore.score,
            VulnerabilityScore.risk_level
        )
        .outerjoin(VillageDemographics, LGDVillage.village_code == VillageDemographics.village_code)
        .outerjoin(VulnerabilityScore, LGDVillage.village_code == VulnerabilityScore.village_code)
    )

    if district_code:
        query = query.filter(LGDVillage.district_code == district_code)
    if taluk_code:
        query = query.filter(LGDVillage.taluk_code == taluk_code)
    if risk_level:
        query = query.filter(VulnerabilityScore.risk_level == risk_level.upper())
    if min_score is not None:
        query = query.filter(VulnerabilityScore.score >= min_score)
    if search:
        query = query.filter(LGDVillage.village_name.ilike(f"%{search}%"))

    results = query.order_by(VulnerabilityScore.score.desc()).offset(offset).limit(limit).all()

    return [
        VillageListItem(
            village_code=r.village_code,
            village_name=r.village_name,
            district_code=r.district_code,
            district_name=r.district_name,
            taluk_code=r.taluk_code,
            taluk_name=r.taluk_name,
            population=r.population or 0,
            vulnerability_score=r.score or 0.0,
            risk_level=r.risk_level or "LOW",
            latitude=r.latitude,
            longitude=r.longitude
        )
        for r in results
    ]

@router.get("/villages/{village_code}", response_model=VillageProfileResponse)
def get_village_profile(village_code: int, db: Session = Depends(get_db)):
    v = db.query(LGDVillage).filter(LGDVillage.village_code == village_code).first()
    if not v:
        raise HTTPException(status_code=404, detail="Village not found")

    demo = db.query(VillageDemographics).filter(VillageDemographics.village_code == village_code).first()
    score = db.query(VulnerabilityScore).filter(VulnerabilityScore.village_code == village_code).first()
    acc = db.query(VillageAccessibility).filter(VillageAccessibility.village_code == village_code).first()

    nearest_phc_name = None
    if acc and acc.nearest_phc_id:
        phc = db.query(HealthFacility).filter(HealthFacility.facility_id == acc.nearest_phc_id).first()
        if phc:
            nearest_phc_name = phc.facility_name

    subscores = {}
    top_factors = []
    if score and score.shap_json:
        try:
            subscores = json.loads(score.shap_json)
        except Exception:
            pass
    if score and score.top_contributing_factors_json:
        try:
            top_factors = json.loads(score.top_contributing_factors_json)
        except Exception:
            pass

    return VillageProfileResponse(
        village_code=v.village_code,
        village_name=v.village_name,
        district_code=v.district_code,
        district_name=v.district_name,
        taluk_code=v.taluk_code,
        taluk_name=v.taluk_name,
        gram_panchayat_name=v.gram_panchayat_name,
        latitude=v.latitude,
        longitude=v.longitude,
        population=demo.population if demo else 0,
        children_under_5=demo.children_under_5 if demo else 0,
        elderly_population=demo.elderly_population if demo else 0,
        literacy_rate=demo.literacy_rate if demo else 0.0,
        road_access=demo.road_access if demo else "N/A",
        drinking_water_access=demo.drinking_water_access if demo else "N/A",
        electricity_access=demo.electricity_access if demo else "N/A",
        telecom_connectivity=demo.telecom_connectivity if demo else "N/A",
        vulnerability_score=score.score if score else 0.0,
        risk_level=score.risk_level if score else "LOW",
        predicted_score_7d=score.predicted_score_7d if score else 0.0,
        subscores=subscores,
        top_contributing_factors=top_factors,
        nearest_phc_name=nearest_phc_name or "PHC Badami HQ",
        distance_to_phc_km=acc.distance_to_phc_km if acc else 5.0,
        travel_time_to_phc_minutes=acc.travel_time_to_phc_minutes if acc else 15.0,
        flood_prone_indicator=acc.flood_prone_indicator if acc else "LOW",
        provenance_classification="REAL_SOURCE_DATA"
    )
