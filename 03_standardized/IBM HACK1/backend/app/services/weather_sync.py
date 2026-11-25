import urllib.request
import json
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.domain import WeatherHazard, LGDVillage, VulnerabilityScore

logger = logging.getLogger("weather_sync")

# Key district centroids in Karnataka for live meteorological telemetry
DISTRICT_COORDINATES = {
    524: {"name": "Bagalkote", "lat": 16.18, "lon": 75.69},
    528: {"name": "Ballari", "lat": 15.14, "lon": 76.92},
    527: {"name": "Belagavi", "lat": 15.85, "lon": 74.50},
    529: {"name": "Bidar", "lat": 17.91, "lon": 77.52},
    525: {"name": "Bengaluru Urban", "lat": 12.97, "lon": 77.59},
    526: {"name": "Bengaluru Rural", "lat": 13.22, "lon": 77.58},
    530: {"name": "Chamarajanagar", "lat": 11.92, "lon": 76.94},
    531: {"name": "Chikkaballapura", "lat": 13.43, "lon": 77.72},
    532: {"name": "Chikkamagaluru", "lat": 13.31, "lon": 75.77},
    533: {"name": "Chitradurga", "lat": 14.22, "lon": 76.40},
    534: {"name": "Dakshina Kannada", "lat": 12.87, "lon": 74.88},
    535: {"name": "Davanagere", "lat": 14.46, "lon": 75.92},
    536: {"name": "Dharwad", "lat": 15.45, "lon": 75.00},
    537: {"name": "Gadag", "lat": 15.43, "lon": 75.63},
    538: {"name": "Hassan", "lat": 13.00, "lon": 76.10},
    539: {"name": "Haveri", "lat": 14.79, "lon": 75.40},
    540: {"name": "Kalaburagi", "lat": 17.33, "lon": 76.83},
    541: {"name": "Kodagu", "lat": 12.42, "lon": 75.73},
    542: {"name": "Kolar", "lat": 13.13, "lon": 78.13},
    543: {"name": "Koppal", "lat": 15.35, "lon": 76.15},
    544: {"name": "Mandya", "lat": 12.52, "lon": 76.89},
    545: {"name": "Mysuru", "lat": 12.29, "lon": 76.63},
    546: {"name": "Raichur", "lat": 16.20, "lon": 77.35},
    547: {"name": "Ramanagara", "lat": 12.72, "lon": 77.28},
    548: {"name": "Shivamogga", "lat": 13.92, "lon": 75.57},
    549: {"name": "Tumakuru", "lat": 13.34, "lon": 77.10},
    550: {"name": "Udupi", "lat": 13.34, "lon": 74.74},
    551: {"name": "Uttara Kannada", "lat": 14.80, "lon": 74.13},
    552: {"name": "Yadgir", "lat": 16.76, "lon": 77.13},
    553: {"name": "Vijayanagara", "lat": 15.27, "lon": 76.38},
}

def sync_live_open_meteo_weather(db: Session) -> dict:
    """
    Fetches real-time meteorological data from Open-Meteo API for Karnataka districts
    and dynamically updates weather_hazards in SQLite database.
    """
    updated_districts = 0
    now_str = datetime.utcnow().isoformat()

    for dist_code, info in DISTRICT_COORDINATES.items():
        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={info['lat']}&longitude={info['lon']}&"
                f"current=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "RuralPulse-Health-Platform/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    curr = data.get("current", {})
                    temp = float(curr.get("temperature_2m", 28.0))
                    humidity = float(curr.get("relative_humidity_2m", 60.0))
                    rain = float(curr.get("precipitation", 0.0))
                    wind = float(curr.get("wind_speed_10m", 10.0))
                    wcode = int(curr.get("weather_code", 0))

                    # Heavy rain / thunderstorm codes in WMO standard
                    is_warning = "YES" if (wcode in [61, 63, 65, 80, 81, 82, 95, 96, 99] or rain > 2.0) else "NO"

                    # Update or insert weather record
                    wh = db.query(WeatherHazard).filter(WeatherHazard.district_code == dist_code).first()
                    if wh:
                        wh.temperature = temp
                        wh.humidity = humidity
                        wh.rainfall = rain
                        wh.wind_speed = wind
                        wh.heavy_rainfall_warning = is_warning
                        wh.retrieval_timestamp = now_str
                    else:
                        wh = WeatherHazard(
                            timestamp=now_str,
                            district_code=dist_code,
                            district_name=info["name"],
                            taluk_code=dist_code * 10,
                            taluk_name=f"{info['name']} Central",
                            latitude=info["lat"],
                            longitude=info["lon"],
                            rainfall=rain,
                            temperature=temp,
                            humidity=humidity,
                            wind_speed=wind,
                            heavy_rainfall_warning=is_warning,
                            source="Open-Meteo Live Telemetry API",
                            retrieval_timestamp=now_str
                        )
                        db.add(wh)
                    updated_districts += 1
        except Exception as e:
            logger.warning(f"Weather sync failed for district {info['name']}: {e}")

    db.commit()

    return {
        "status": "SUCCESS",
        "synced_districts": updated_districts,
        "timestamp": now_str,
        "source": "Open-Meteo Live Meteorological Telemetry API"
    }
