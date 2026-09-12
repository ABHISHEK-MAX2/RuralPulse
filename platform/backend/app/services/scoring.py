"""7-Dimension Composite Risk Scoring Engine for Karnataka Rural Healthcare Intelligence."""

def calculate_village_risk_score(village_data: dict) -> dict:
    distance_phc = float(village_data.get("distance_to_phc_km", 0.0))
    travel_time = float(village_data.get("travel_time_to_phc_minutes", 0.0))
    road_access = str(village_data.get("road_accessibility", "ALL_WEATHER"))
    flood_hazard = str(village_data.get("flood_prone_indicator", "LOW"))
    population = int(village_data.get("population", 0))
    anc_deficit = float(village_data.get("anc_deficit_pct", 20.0))
    water_quality = float(village_data.get("water_quality_index", 80.0))

    # Dimension Weights
    score_phc = min((distance_phc / 25.0) * 30.0, 30.0)
    score_travel = min((travel_time / 60.0) * 20.0, 20.0)
    score_road = 20.0 if road_access == "UNPAVED" else (15.0 if road_access == "SEASONAL_UNPAVED" else 5.0)
    score_flood = 15.0 if flood_hazard == "HIGH" else (10.0 if flood_hazard == "MEDIUM" else 2.0)
    score_anc = min((anc_deficit / 50.0) * 10.0, 10.0)
    score_water = max((100.0 - water_quality) * 0.05, 0.0)

    composite_score = round(score_phc + score_travel + score_road + score_flood + score_anc + score_water, 1)
    composite_score = min(max(composite_score, 0.0), 100.0)

    if composite_score >= 75.0:
        category = "CRITICAL"
    elif composite_score >= 60.0:
        category = "HIGH"
    elif composite_score >= 40.0:
        category = "MEDIUM"
    else:
        category = "LOW"

    return {
        "risk_score": composite_score,
        "risk_category": category,
        "factors": {
            "phc_distance_pts": round(score_phc, 1),
            "travel_time_pts": round(score_travel, 1),
            "road_access_pts": round(score_road, 1),
            "flood_hazard_pts": round(score_flood, 1),
            "anc_deficit_pts": round(score_anc, 1),
            "water_quality_pts": round(score_water, 1)
        }
    }
