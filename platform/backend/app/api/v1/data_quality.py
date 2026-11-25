from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()

class DataProvenanceSource(BaseModel):
    layer_number: int
    code: str
    name: str
    records: int
    provenance: str  # REAL_SOURCE_DATA, DERIVED_DATA, MODEL_OUTPUT, NOT_PUBLICLY_AVAILABLE, SYNTHETIC_DEMO_DATA
    source_org: str
    last_synced: str
    quality_status: str
    missingness_pct: float

@router.get("/sources", response_model=List[DataProvenanceSource])
def get_data_sources_provenance():
    return [
        DataProvenanceSource(layer_number=1, code="LAYER_01", name="LGD Administrative Master", records=30771, provenance="REAL_SOURCE_DATA", source_org="Govt of India LGD Portal", last_synced="2026-09-12 18:00 UTC", quality_status="EXCELLENT", missingness_pct=0.0),
        DataProvenanceSource(layer_number=2, code="LAYER_02", name="Village Demographics & Infra", records=30771, provenance="REAL_SOURCE_DATA", source_org="Census & Rural Dev Dept", last_synced="2026-09-12 18:00 UTC", quality_status="GOOD", missingness_pct=0.8),
        DataProvenanceSource(layer_number=3, code="LAYER_03", name="Health Facility Master", records=721, provenance="REAL_SOURCE_DATA", source_org="National Health Mission (NHM)", last_synced="2026-09-12 15:30 UTC", quality_status="EXCELLENT", missingness_pct=0.0),
        DataProvenanceSource(layer_number=4, code="LAYER_04", name="Health Service Utilization", records=721, provenance="DERIVED_DATA", source_org="Health Department Analytics", last_synced="2026-09-12 14:00 UTC", quality_status="GOOD", missingness_pct=2.1),
        DataProvenanceSource(layer_number=5, code="LAYER_05", name="Health Indicators", records=32, provenance="REAL_SOURCE_DATA", source_org="NFHS-5 & State Health Survey", last_synced="2026-09-10 09:00 UTC", quality_status="EXCELLENT", missingness_pct=0.0),
        DataProvenanceSource(layer_number=6, code="LAYER_06", name="Anganwadi Nutrition Data", records=481, provenance="SYNTHETIC_DEMO_DATA", source_org="WCD Department (Demo Mode)", last_synced="2026-09-12 12:00 UTC", quality_status="VERIFIED", missingness_pct=1.4),
        DataProvenanceSource(layer_number=7, code="LAYER_07", name="Weather Hazard Real-Time", records=32, provenance="REAL_SOURCE_DATA", source_org="KSNDMC Weather Portal", last_synced="2026-09-12 23:00 UTC", quality_status="EXCELLENT", missingness_pct=0.0),
        DataProvenanceSource(layer_number=8, code="LAYER_08", name="Village Accessibility Matrix", records=30771, provenance="DERIVED_DATA", source_org="GIS Spatial Engine", last_synced="2026-09-12 18:00 UTC", quality_status="EXCELLENT", missingness_pct=0.0),
        DataProvenanceSource(layer_number=9, code="LAYER_09", name="Operational Resources (DVDMS)", records=21, provenance="NOT_PUBLICLY_AVAILABLE", source_org="Authorized Govt Access Required", last_synced="2026-09-12 00:00 UTC", quality_status="RESTRICTED", missingness_pct=0.0),
        DataProvenanceSource(layer_number=10, code="LAYER_10", name="MMU Operations Log", records=11, provenance="REAL_SOURCE_DATA", source_org="Karnataka MMU Fleet System", last_synced="2026-09-12 21:00 UTC", quality_status="EXCELLENT", missingness_pct=0.0),
        DataProvenanceSource(layer_number=11, code="LAYER_11", name="AI Vulnerability Score Output", records=30771, provenance="MODEL_OUTPUT", source_org="7-Dim XAI Risk Model", last_synced="2026-09-12 23:15 UTC", quality_status="VALIDATED", missingness_pct=0.0)
    ]
