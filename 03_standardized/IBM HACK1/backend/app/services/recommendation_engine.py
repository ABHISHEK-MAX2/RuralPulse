import json
import urllib.request
import logging
from typing import List, Dict, Any
from app.config import settings

logger = logging.getLogger("recommendation_engine")

class RecommendationEngine:
    """
    AI Decision Support & Action Recommendation Engine for Rural Karnataka.
    Primary: Groq LLM (groq/compound-mini or llama).
    Fallback: Deterministic Rule-Based AI Engine if Groq API quota/network fails.
    """
    
    @staticmethod
    def _generate_via_groq(
        village_code: int,
        village_name: str,
        vulnerability_score: float,
        risk_level: str,
        subscores: Dict[str, float],
        accessibility: Dict[str, Any],
        anganwadi: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        if not settings.GROQ_API_KEY or settings.GROQ_API_KEY.strip() == "":
            raise ValueError("Groq API Key not configured")

        prompt = f"""
You are an expert AI Public Health Officer for Karnataka State Health Department.
Generate 2-3 specific health intervention recommendations for village '{village_name}' (LGD Code: {village_code}).

Village Metrics:
- Vulnerability Score: {vulnerability_score}/100 ({risk_level} Risk)
- PHC Travel Time: {accessibility.get('travel_time_to_phc_minutes', 30)} mins ({accessibility.get('distance_to_phc_km', 5)} km)
- Malnutrition SAM cases: {anganwadi.get('sam_cases', 0)}, MAM cases: {anganwadi.get('mam_cases', 0)}
- Healthcare Access Subscore: {subscores.get('healthcare_access', 0)}
- Maternal Health Subscore: {subscores.get('maternal_child_health', 0)}
- Immunization Subscore: {subscores.get('immunization_coverage', 0)}

Return ONLY a JSON list of objects matching this exact schema:
[
  {{
    "village_code": {village_code},
    "action": "Action Name",
    "reason": "Detailed rationale based on village metrics",
    "priority": "CRITICAL",
    "expected_impact": "Expected clinical or operational impact",
    "required_resources": "Required vehicles, personnel, or medical supplies",
    "suggested_deadline": "Within 48 Hours",
    "confidence": 0.95,
    "supporting_indicators": ["Vulnerability Score: {vulnerability_score}/100"]
  }}
]
"""

        payload = {
            "model": settings.GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are a public health AI assistant. Output strictly a JSON array of recommendations."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_completion_tokens": 1000
        }

        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (KarnatakaHealthAI/1.0)"
            }
        )

        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            content = res_data["choices"][0]["message"]["content"].strip()
            
            # Clean markdown fenced code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            parsed = json.loads(content)
            if isinstance(parsed, list) and len(parsed) > 0:
                for item in parsed:
                    item["source"] = f"Groq LLM ({settings.GROQ_MODEL})"
                return parsed
            raise ValueError("Invalid JSON list returned by Groq")

    @staticmethod
    def _generate_deterministic(
        village_code: int,
        village_name: str,
        vulnerability_score: float,
        risk_level: str,
        subscores: Dict[str, float],
        accessibility: Dict[str, Any],
        anganwadi: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        recommendations = []
        
        try:
            travel_time = float(accessibility.get("travel_time_to_phc_minutes", 30.0) or 30.0)
        except (ValueError, TypeError):
            travel_time = 30.0

        try:
            sam_cases = int(float(anganwadi.get("sam_cases", 0) or 0))
        except (ValueError, TypeError):
            sam_cases = 0

        try:
            mam_cases = int(float(anganwadi.get("mam_cases", 0) or 0))
        except (ValueError, TypeError):
            mam_cases = 0

        # 1. Deploy Mobile Medical Unit (MMU)
        if vulnerability_score >= 50.0 or subscores.get("healthcare_access", 0) >= 40.0:
            recommendations.append({
                "village_code": village_code,
                "action": "Deploy Mobile Medical Unit (MMU)",
                "reason": f"Village has high overall vulnerability ({vulnerability_score}/100) and travel time to nearest PHC is {travel_time:.0f} minutes.",
                "priority": "CRITICAL" if risk_level in ("CRITICAL", "HIGH") else "HIGH",
                "expected_impact": "Direct primary healthcare screening, diagnostic tests, and medicine dispensing for 100+ vulnerable residents.",
                "required_resources": "MMU Vehicle with Doctor, Nurse, ANM, Diagnostic Kit, Basic Medicines",
                "suggested_deadline": "Within 48 Hours" if risk_level == "CRITICAL" else "Within 7 Days",
                "confidence": 0.92,
                "supporting_indicators": [
                    f"Vulnerability Score: {vulnerability_score}/100",
                    f"Travel time to PHC: {travel_time:.0f} min",
                    f"Risk Level: {risk_level}"
                ],
                "source": "Deterministic Rule-Based Engine (Fallback)"
            })

        # 2. SAM/MAM Nutrition Screening & Intervention Drive
        if sam_cases > 0 or mam_cases > 2 or subscores.get("nutrition_malnutrition", 0) >= 30.0:
            recommendations.append({
                "village_code": village_code,
                "action": "Severe Malnutrition Screening & THR Outreach Drive",
                "reason": f"Active malnutrition burden detected ({sam_cases} Severe Acute Malnutrition & {mam_cases} Moderate Acute Malnutrition cases registered at Anganwadi).",
                "priority": "CRITICAL" if sam_cases > 0 else "HIGH",
                "expected_impact": "Provide immediate therapeutic nutrition supplements (EDNRF/THR), medical evaluation by PHC officer, and NRC referral if required.",
                "required_resources": "Anganwadi Worker, Pediatrician/PHC MO, Energy Dense Nutritional Foods, IFA Syrups",
                "suggested_deadline": "Within 3 Days",
                "confidence": 0.95,
                "supporting_indicators": [
                    f"SAM Cases: {sam_cases}",
                    f"MAM Cases: {mam_cases}",
                    f"Nutrition Subscore: {subscores.get('nutrition_malnutrition', 0):.1f}"
                ],
                "source": "Deterministic Rule-Based Engine (Fallback)"
            })

        # 3. Schedule Special Immunization Outreach Drive
        if subscores.get("immunization_coverage", 0) >= 25.0 or risk_level in ("CRITICAL", "HIGH"):
            recommendations.append({
                "village_code": village_code,
                "action": "Schedule Special Immunization Outreach Drive",
                "reason": "District under-5 full immunization coverage displays deficit compared to state targets.",
                "priority": "HIGH",
                "expected_impact": "Achieve 100% full immunization coverage for zero-dose and drop-out children under 5.",
                "required_resources": "ANM, Cold Chain Carrier Box, Pentavalent/MR Vaccines, Asha Workers",
                "suggested_deadline": "Within 10 Days",
                "confidence": 0.88,
                "supporting_indicators": [
                    f"Immunization Subscore: {subscores.get('immunization_coverage', 0):.1f}"
                ],
                "source": "Deterministic Rule-Based Engine (Fallback)"
            })

        # 4. Maternal Health & ANC Screening Camp
        if subscores.get("maternal_child_health", 0) >= 25.0:
            recommendations.append({
                "village_code": village_code,
                "action": "Conduct Maternal & High-Risk Pregnancy ANC Camp",
                "reason": "First trimester ANC registration deficit and rural travel barrier to institutional delivery.",
                "priority": "HIGH",
                "expected_impact": "Identify high-risk pregnant mothers, provide HB screening, IFA tablets, and institutional delivery counseling.",
                "required_resources": "OB/GYN or Trained Staff Nurse, Hemoglobinometer, Ultrasonography Access, Ambulance Linkage",
                "suggested_deadline": "Within 7 Days",
                "confidence": 0.90,
                "supporting_indicators": [
                    f"Maternal Care Subscore: {subscores.get('maternal_child_health', 0):.1f}"
                ],
                "source": "Deterministic Rule-Based Engine (Fallback)"
            })

        return recommendations

from app.services.watsonx_engine import WatsonXEngine

class RecommendationEngine:
    """
    AI Decision Support & Action Recommendation Engine for Rural Karnataka.
    Tier 1: IBM watsonx.ai (Granite-3-8b-instruct).
    Tier 2: Groq LLM API (groq/compound-mini).
    Tier 3: Deterministic Rule-Based Engine (Guaranteed zero-downtime fallback).
    """

    @classmethod
    def generate_recommendations_for_village(
        cls,
        village_code: int,
        village_name: str,
        vulnerability_score: float,
        risk_level: str,
        subscores: Dict[str, float],
        top_factors: List[Dict[str, Any]],
        accessibility: Dict[str, Any],
        anganwadi: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        # 1. Tier 1 Attempt: IBM watsonx.ai Engine
        try:
            return WatsonXEngine.generate_recommendations(
                village_code=village_code,
                village_name=village_name,
                vulnerability_score=vulnerability_score,
                risk_level=risk_level,
                subscores=subscores,
                accessibility=accessibility,
                anganwadi=anganwadi
            )
        except Exception as wx_err:
            logger.info(f"IBM watsonx.ai engine skipped/failed ({wx_err}). Trying Groq LLM.")

        # 2. Tier 2 Attempt: Groq LLM API
        try:
            return cls._generate_via_groq(
                village_code=village_code,
                village_name=village_name,
                vulnerability_score=vulnerability_score,
                risk_level=risk_level,
                subscores=subscores,
                accessibility=accessibility,
                anganwadi=anganwadi
            )
        except Exception as groq_err:
            logger.warning(f"Groq LLM generation failed ({groq_err}). Falling back to Deterministic Engine.")

        # 3. Tier 3 Attempt: Deterministic Rule-Based Engine (Guaranteed Fallback)
        return cls._generate_deterministic(
            village_code=village_code,
            village_name=village_name,
            vulnerability_score=vulnerability_score,
            risk_level=risk_level,
            subscores=subscores,
            accessibility=accessibility,
            anganwadi=anganwadi
        )
