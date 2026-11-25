from app.services.scoring_engine import VulnerabilityScoringEngine

def test_vulnerability_scoring_calculation():
    demographics = {
        "population": 1500,
        "children_under_5": 150,
        "elderly_population": 120,
        "literacy_rate": 65.0,
        "road_access": "Unpaved Gravel",
        "drinking_water_access": "Borewell",
        "telecom_connectivity": "Poor 2G"
    }
    accessibility = {
        "distance_to_phc_km": 12.5,
        "travel_time_to_phc_minutes": 45.0,
        "road_type": "Unpaved Gravel",
        "flood_prone_indicator": "HIGH"
    }
    district_indicators = {
        "anc_coverage": 65.0,
        "institutional_delivery": 80.0,
        "immunization_coverage": 70.0
    }
    anganwadi = {
        "children_screened": 60,
        "sam_cases": 3,
        "mam_cases": 5
    }
    weather = {
        "rainfall": 45.0,
        "heavy_rainfall_warning": "YES"
    }
    facility_utilization = {
        "opd": 800
    }

    score, risk_lvl, subscores, top_factors, pred_7d = VulnerabilityScoringEngine.compute_village_vulnerability(
        demographics=demographics,
        accessibility=accessibility,
        district_indicators=district_indicators,
        anganwadi=anganwadi,
        weather=weather,
        facility_utilization=facility_utilization
    )

    assert 0.0 <= score <= 100.0
    assert risk_lvl in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
    assert "healthcare_access" in subscores
    assert len(top_factors) > 0
    assert pred_7d >= score
