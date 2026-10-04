from __future__ import annotations

import math

EARTH_KM = 6371.0
KRAKOW_PODGORZE = {
    "lat": 50.0415,
    "lng": 19.9493,
    "label": "Podgórze, Kraków",
}


def haversine_km(a: dict, b: dict) -> float:
    to_rad = math.radians
    d_lat = to_rad(b["lat"] - a["lat"])
    d_lng = to_rad(b["lng"] - a["lng"])
    lat1 = to_rad(a["lat"])
    lat2 = to_rad(b["lat"])
    h = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lng / 2) ** 2
    return 2 * EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


def offset_latlng(origin: dict, east_m: float, north_m: float) -> dict:
    d_lat = north_m / 111_320
    d_lng = east_m / (111_320 * math.cos(math.radians(origin["lat"])))
    return {"lat": origin["lat"] + d_lat, "lng": origin["lng"] + d_lng}


def format_distance(km: float) -> str:
    if km < 0.08:
        return "tuż obok"
    if km < 1:
        return f"{round(km * 1000)} m"
    return f"{km:.1f} km".replace(".", ",")


def format_approx_distance(km: float) -> str:
    if km < 0.12:
        return "w Twojej okolicy"
    if km < 1:
        meters = int(round(km * 10) * 100)
        return f"ok. {meters} m"
    rounded = round(km * 2) / 2
    return f"ok. {rounded:.1f} km".replace(".", ",")


def format_near_distance(km: float) -> str:
    meters = km * 1000
    if meters < 280:
        return "tuż obok"
    if meters <= 2000:
        stepped = int(math.ceil(meters / 500) * 500)
        if stepped < 1000:
            return f"ok. {stepped} m"
        text = f"{stepped / 1000:.1f}".replace(".", ",")
        if text.endswith(",0"):
            text = text[:-2]
        return f"ok. {text} km"
    rounded = round(km)
    return f"ok. {rounded} km"


def jitter_from_id(seed_id: str) -> tuple[float, float]:
    n = sum((i + 1) * ord(ch) for i, ch in enumerate(seed_id))
    east = ((n % 19) - 9) * 11
    north = ((n % 15) - 7) * 11
    return east, north
