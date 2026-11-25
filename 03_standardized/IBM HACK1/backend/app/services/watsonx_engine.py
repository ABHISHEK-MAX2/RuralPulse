import json
import urllib.request
import urllib.parse
import logging
from typing import List, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger("watsonx_engine")

class WatsonXEngine:
    """
    IBM watsonx.ai Text Generation Engine for Karnataka Rural Healthcare Platform.
    Uses IBM Cloud IAM OAuth or Direct WatsonX API deployment endpoints to generate
    AI public health recommendations using IBM Granite models (ibm/granite-3-8b-instruct).
    """

    _cached_token: Optional[str] = None

    @classmethod
    def get_iam_token(cls) -> Optional[str]:
        if cls._cached_token:
            return cls._cached_token

        if not settings.WATSONX_API_KEY:
            return None

        try:
            url = "https://iam.cloud.ibm.com/identity/token"
            data = urllib.parse.urlencode({
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": settings.WATSONX_API_KEY
            }).encode("utf-8")

            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json"
                }
            )

            with urllib.request.urlopen(req, timeout=4) as res:
                res_data = json.loads(res.read().decode("utf-8"))
                cls._cached_token = res_data.get("access_token")
                return cls._cached_token
        except Exception as e:
            logger.warning(f"IBM IAM token request failed: {e}")
            return None

    @classmethod
    def generate_recommendations(
        cls,
        village_code: int,
        village_name: str,
        vulnerability_score: float,
        risk_level: str,
        subscores: Dict[str, float],
        accessibility: Dict[str, Any],
        anganwadi: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Attempts generation using IBM watsonx.ai (Granite-3-8b / Deployment).
        If watsonx authentication/quota fails, raises Exception so caller can failover.
        """
        token = cls.get_iam_token() or settings.WATSONX_API_KEY
        if not token:
            raise ValueError("IBM watsonx credentials unavailable")

        prompt = f"""<|system|>
You are IBM watsonx.ai Public Health Advisor for Karnataka State Health Department.
Generate 2-3 structured health interventions for village '{village_name}' (LGD: {village_code}).

Vulnerability Metrics:
- Score: {vulnerability_score}/100 ({risk_level} Risk)
- PHC Travel Time: {accessibility.get('travel_time_to_phc_minutes', 30)} mins
- Malnutrition: {anganwadi.get('sam_cases', 0)} SAM, {anganwadi.get('mam_cases', 0)} MAM
- Access Subscore: {subscores.get('healthcare_access', 0)}
- Maternal Care Subscore: {subscores.get('maternal_child_health', 0)}
- Immunization Subscore: {subscores.get('immunization_coverage', 0)}

Return ONLY JSON format list:
[
  {{
    "village_code": {village_code},
    "action": "Action Name",
    "reason": "Rationale based on metrics",
    "priority": "CRITICAL",
    "expected_impact": "Impact",
    "required_resources": "Resources needed",
    "suggested_deadline": "Within 48 Hours",
    "confidence": 0.96,
    "supporting_indicators": ["Vulnerability Score: {vulnerability_score}"]
  }}
]
<|user|>
Generate recommendations for {village_name}.
<|assistant|>
"""

        # First attempt: Direct watsonx Text Generation API
        url = f"{settings.WATSONX_URL}/ml/v1/text/generation?version=2023-05-29"
        payload = {
            "model_id": settings.WATSONX_MODEL_ID,
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 800,
                "min_new_tokens": 10
            },
            "project_id": settings.WATSONX_PROJECT_ID
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                results = res_data.get("results", [])
                if results and "generated_text" in results[0]:
                    text = results[0]["generated_text"].strip()
                    if text.startswith("```json"):
                        text = text[7:]
                    if text.startswith("```"):
                        text = text[3:]
                    if text.endswith("```"):
                        text = text[:-3]
                    text = text.strip()
                    parsed = json.loads(text)
                    if isinstance(parsed, list) and len(parsed) > 0:
                        for item in parsed:
                            item["source"] = f"IBM watsonx.ai ({settings.WATSONX_MODEL_ID})"
                        return parsed
        except Exception as primary_err:
            logger.warning(f"IBM watsonx.ai text generation failed: {primary_err}")

        # Second attempt: Deployment endpoint
        if settings.WATSONX_DEPLOYMENT_ID:
            dep_url = f"{settings.WATSONX_URL}/ml/v1/deployments/{settings.WATSONX_DEPLOYMENT_ID}/text/generation?version=2023-05-29"
            dep_payload = {
                "input": prompt,
                "parameters": {"max_new_tokens": 600}
            }
            dep_req = urllib.request.Request(
                dep_url,
                data=json.dumps(dep_payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(dep_req, timeout=4) as dep_res:
                dep_data = json.loads(dep_res.read().decode("utf-8"))
                dep_text = dep_data.get("results", [{}])[0].get("generated_text", "").strip()
                parsed = json.loads(dep_text)
                if isinstance(parsed, list) and len(parsed) > 0:
                    for item in parsed:
                        item["source"] = f"IBM watsonx.ai Deployment ({settings.WATSONX_DEPLOYMENT_ID[:8]})"
                    return parsed

        raise ValueError("IBM watsonx.ai generation returned invalid structure")
