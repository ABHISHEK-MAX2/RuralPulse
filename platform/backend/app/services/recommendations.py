"""Intervention Recommendation Engine for Rural Healthcare Intelligence."""

def generate_village_interventions(risk_category: str, risk_factors: dict) -> list[dict]:
    interventions = []

    if risk_category in ["CRITICAL", "HIGH"]:
        interventions.append({
            "title": "Priority MMU Mobile Health Camp Dispatch",
            "type": "MMU_DISPATCH",
            "description": "Schedule weekly MMU visit for maternal ANC checkups and child immunization.",
            "priority": "URGENT"
        })
        interventions.append({
            "title": "DVDMS Vaccine & Drug Cold-Chain Replenishment",
            "type": "SUPPLY_CHAIN",
            "description": "Refill essential vaccine and maternal drug buffer stock via DVDMS portal.",
            "priority": "HIGH"
        })
        interventions.append({
            "title": "ASHA Door-to-Door High-Risk Tracking",
            "type": "ASHA_TRACKING",
            "description": "Activate ASHA worker door-to-door tracking for high-risk pregnant women.",
            "priority": "HIGH"
        })

    if risk_factors.get("flood_hazard_pts", 0) > 10.0:
        interventions.append({
            "title": "Monsoon Transport Preparedness Protocol",
            "type": "INFRASTRUCTURE",
            "description": "Pre-position 4WD emergency transport unit at nearest PHC hub.",
            "priority": "MEDIUM"
        })

    return interventions
