from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from geo import format_near_distance, haversine_km, offset_latlng
from seed import (
    AGE_BAND_LABEL,
    AUDIENCE_LABEL,
    CATEGORY_LABEL,
    EVENT_SEEDS,
    GENDER_LABEL,
    HAPPENING_SEEDS,
    KIND_SWAP_LABEL,
    PARENT_SEEDS,
    PLACE_KIND_LABEL,
    PLACE_SEEDS,
    PLATFORM_LABEL,
    SWAP_SEEDS,
    WANT_LABEL,
    DEFAULT_PROFILE,
    INTEREST_LABEL,
    SEEKING_LABEL,
    CHAT_REPLIES,
    NOTICE_SEEDS,
    THREAD_SEEDS,
    area_of,
    area_phrase,
    bands_close,
    normalize_kids,
    normalize_seeking,
    public_kid,
    seed_area,
)

ROOT = Path(__file__).parent
DB_PATH = ROOT / "village.db"
STATIC = ROOT / "static"

app = FastAPI(title="mamy wioskę")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                kind TEXT NOT NULL,
                when_text TEXT NOT NULL,
                place TEXT NOT NULL,
                lat REAL NOT NULL,
                lng REAL NOT NULL,
                spots INTEGER NOT NULL,
                blurb TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS joins (
                event_id TEXT NOT NULL,
                who TEXT NOT NULL,
                PRIMARY KEY (event_id, who)
            );
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                text TEXT NOT NULL,
                at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS swaps (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                platform TEXT NOT NULL,
                url TEXT NOT NULL,
                note TEXT NOT NULL,
                lat REAL NOT NULL,
                lng REAL NOT NULL,
                who TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS trust (
                parent_id TEXT PRIMARY KEY,
                met INTEGER NOT NULL DEFAULT 0,
                reported INTEGER NOT NULL DEFAULT 0,
                starred INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS notice_read (
                notice_id TEXT PRIMARY KEY
            );
            CREATE TABLE IF NOT EXISTS thread_state (
                parent_id TEXT PRIMARY KEY,
                unread INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS place_recs (
                place_id TEXT PRIMARY KEY,
                recommended INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS places (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                kind TEXT NOT NULL,
                tag TEXT NOT NULL,
                note TEXT NOT NULL,
                lat REAL NOT NULL,
                lng REAL NOT NULL,
                who TEXT NOT NULL
            );
            """
        )
        cols = {row[1] for row in conn.execute("PRAGMA table_info(trust)")}
        if "starred" not in cols:
            conn.execute("ALTER TABLE trust ADD COLUMN starred INTEGER NOT NULL DEFAULT 0")
    seed_social()


def parent_card(parent_id: str) -> dict:
    seed = next((p for p in PARENT_SEEDS if p["id"] == parent_id), None)
    if not seed:
        return {"id": parent_id, "name": parent_id.title()}
    return {
        "id": seed["id"],
        "name": seed["name"],
        "kid_label": public_kid(seed["gender"], seed["age_band"]),
    }


def seed_social() -> None:
    with db() as conn:
        for row in THREAD_SEEDS:
            existing = conn.execute(
                "SELECT COUNT(*) AS n FROM messages WHERE parent_id = ?",
                (row["parent_id"],),
            ).fetchone()["n"]
            if existing:
                continue
            conn.execute(
                "INSERT INTO messages (parent_id, sender, text, at) VALUES (?, ?, ?, ?)",
                (row["parent_id"], row["sender"], row["text"], row["at"]),
            )
            conn.execute(
                "INSERT OR REPLACE INTO thread_state (parent_id, unread) VALUES (?, 1)",
                (row["parent_id"],),
            )
        for event_id in ("kawa", "cafe-lipa"):
            conn.execute(
                "INSERT OR IGNORE INTO joins (event_id, who) VALUES (?, 'sylwia')",
                (event_id,),
            )


init_db()


class VillageQuery(BaseModel):
    district_id: str = "podgorze"
    area_id: str = ""
    want: str = "wszyscy"
    similar_age: bool = False
    lat: float | None = None
    lng: float | None = None
    radius_km: float | None = None
    seeking: list[str] = []


class EventIn(BaseModel):
    title: str
    kind: str = "inicjatywa"
    when: str = "Wkrótce"
    place: str = "W Twojej okolicy"
    lat: float
    lng: float


class MessageIn(BaseModel):
    parent_id: str
    text: str


class JoinIn(BaseModel):
    event_id: str
    joined: bool = True


class SwapIn(BaseModel):
    title: str
    platform: str = "osiedle"
    url: str = ""
    note: str = ""
    lat: float
    lng: float


class PlaceIn(BaseModel):
    name: str
    kind: str = "miejsce"
    tag: str = ""
    note: str = ""
    lat: float
    lng: float


def pin_from_seed(seed: dict, seed_id: str | None = None) -> tuple[dict, str, str]:
    district_id, area_id = seed_area(seed_id or seed.get("id") or "", seed)
    center = area_of(area_id, district_id)
    loc = offset_latlng(center, seed.get("east") or 0, seed.get("north") or 0)
    return loc, district_id, area_id


def distance_fields(origin: dict, loc: dict) -> dict:
    km = haversine_km(origin, loc)
    return {"distance_km": round(km, 3), "distance": format_near_distance(km)}


def me_origin() -> dict:
    profile = read_profile()
    return area_of(profile.get("area_id") or "stare-podgorze", profile.get("district_id") or "podgorze")


def nearby_swaps(origin: dict) -> list[dict]:
    with db() as conn:
        rows = conn.execute("SELECT * FROM swaps").fetchall()
    items: list[dict] = []
    for seed in SWAP_SEEDS:
        loc, _item_district, _item_area = pin_from_seed(seed)
        items.append(
            {
                **{k: v for k, v in seed.items() if k not in {"east", "north", "lat", "lng"}},
                **distance_fields(origin, loc),
                "platform_label": PLATFORM_LABEL.get(seed.get("platform") or "osiedle", "Osiedle"),
                "kind_label": KIND_SWAP_LABEL.get(seed.get("kind") or "link", "Link"),
                "photo": seed.get("photo") or "/static/img/photos/hero-swap.jpg",
            }
        )
    for row in rows:
        loc = {"lat": row["lat"], "lng": row["lng"]}
        items.append(
            {
                "id": row["id"],
                "title": row["title"],
                "platform": row["platform"],
                "url": row["url"],
                "note": row["note"],
                "who": row["who"],
                **distance_fields(origin, loc),
                "platform_label": PLATFORM_LABEL.get(row["platform"] or "osiedle", "Osiedle"),
                "kind_label": KIND_SWAP_LABEL.get("link", "Link"),
                "photo": "/static/img/photos/hero-swap.jpg",
            }
        )
    return sorted(items, key=lambda s: s.get("distance_km") or 0)


def place_rec_map() -> dict[str, bool]:
    with db() as conn:
        rows = conn.execute("SELECT place_id, recommended FROM place_recs").fetchall()
    return {row["place_id"]: bool(row["recommended"]) for row in rows}


def place_is_recommended(place_id: str, source: str, recs: dict[str, bool]) -> bool:
    if place_id in recs:
        return recs[place_id]
    return source == "user"


def serialize_place(seed: dict, origin: dict, recs: dict[str, bool], loc: dict | None = None) -> dict:
    if loc is None:
        loc, _item_district, _item_area = pin_from_seed(seed)
    source = seed.get("source") or "admin"
    kind = seed.get("kind") or "miejsce"
    if kind not in PLACE_KIND_LABEL:
        kind = "miejsce"
    recommended = place_is_recommended(seed["id"], source, recs)
    return {
        **{k: v for k, v in seed.items() if k not in {"east", "north", "lat", "lng", "verified"}},
        **distance_fields(origin, loc),
        "kind": kind,
        "kind_label": PLACE_KIND_LABEL[kind],
        "source": source,
        "photo": seed.get("photo") or "/static/img/photos/place-kawa.jpg",
        "verified": recommended,
        "recommended": recommended,
    }


def nearby_places(origin: dict) -> list[dict]:
    recs = place_rec_map()
    out = [serialize_place(seed, origin, recs) for seed in PLACE_SEEDS]
    with db() as conn:
        rows = conn.execute("SELECT * FROM places").fetchall()
    seen = {item["id"] for item in out}
    for row in rows:
        if row["id"] in seen:
            continue
        loc = {"lat": row["lat"], "lng": row["lng"]}
        out.append(
            serialize_place(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "kind": row["kind"],
                    "source": "user",
                    "tag": row["tag"] or PLACE_KIND_LABEL.get(row["kind"], "Miejsce").lower(),
                    "note": row["note"],
                    "by": row["who"],
                    "photo": "/static/img/photos/place-kawa.jpg",
                },
                origin,
                recs,
                loc,
            )
        )
    return sorted(out, key=lambda p: (not p["recommended"], p.get("distance_km") or 0, p["name"]))


def nearby_parents(
    want: str,
    similar_age: bool = False,
    origin: dict | None = None,
    radius_km: float | None = None,
    seeking_filter: list[str] | None = None,
) -> list[dict]:
    profile = read_profile()
    mine = [kid["age_band"] for kid in normalize_kids(profile.get("kids"))]
    my_seeking = set(profile.get("seeking") or [])
    wanted = set(normalize_seeking(seeking_filter))
    match_against = wanted or my_seeking
    center = origin or me_origin()
    out = []
    for seed in PARENT_SEEDS:
        loc, _item_district, _item_area = pin_from_seed(seed)
        km = haversine_km(center, loc)
        if radius_km is not None and km > radius_km + 0.001:
            continue
        if want != "wszyscy" and seed["want"] != want:
            continue
        if similar_age and not bands_close(seed["age_band"], mine):
            continue
        seeking = seed.get("seeking") or []
        if wanted and not wanted.intersection(seeking):
            continue
        overlap = [sid for sid in seeking if sid in match_against]
        item = {k: v for k, v in seed.items() if k not in {"east", "north", "gender", "age_band", "district_id", "area_id", "window"}}
        item.update(
            {
                **distance_fields(center, loc),
                "want_label": WANT_LABEL[seed["want"]],
                "kid_label": public_kid(seed["gender"], seed["age_band"]),
                "age_band": seed["age_band"],
                "gender": seed["gender"],
                "seeking": seeking,
                "overlap": overlap,
                "overlap_labels": [SEEKING_LABEL.get(sid, sid) for sid in overlap],
                "match_score": len(overlap),
            }
        )
        out.append(item)
    return sorted(out, key=lambda p: (p["distance_km"], -p["match_score"], p["name"]))


def enrich_happening(item: dict, joined: set[str]) -> dict:
    category = item.get("category") or "inicjatywa"
    audience = item.get("audience") or "wszyscy"
    free = bool(item.get("free", True))
    return {
        **item,
        "joined": item["id"] in joined,
        "free": free,
        "price_label": "Darmowe" if free else "Płatne",
        "category_label": CATEGORY_LABEL.get(category, "Wioska"),
        "audience_label": AUDIENCE_LABEL.get(audience, "Dla opiekunów"),
        "horizon": item.get("horizon") or "tydzien",
        "art": item.get("art") or "park",
        "photo": item.get("photo") or "/static/img/park.svg",
    }


def nearby_happenings(origin: dict) -> list[dict]:
    with db() as conn:
        rows = conn.execute("SELECT * FROM events").fetchall()
        joined = {
            row["event_id"]
            for row in conn.execute("SELECT event_id FROM joins WHERE who = 'sylwia'")
        }

    items: list[dict] = []
    for seed in HAPPENING_SEEDS:
        loc, _d, _a = pin_from_seed(seed)
        items.append(
            {
                **{k: v for k, v in seed.items() if k not in {"east", "north", "district_id", "area_id", "lat", "lng"}},
                **distance_fields(origin, loc),
            }
        )
    for seed in EVENT_SEEDS:
        loc, _d, _a = pin_from_seed(seed)
        items.append(
            {
                "id": seed["id"],
                "title": seed["title"],
                "source": "Sąsiadki z okolicy",
                "category": seed.get("category") or "inicjatywa",
                "audience": "wszyscy",
                "when": seed["when"],
                "place": seed["place"],
                "blurb": seed["blurb"],
                "spots": seed["spots"],
                "horizon": seed.get("horizon") or "tydzien",
                "art": seed.get("art") or "park",
                "photo": seed.get("photo") or "/static/img/park.svg",
                "free": True,
                **distance_fields(origin, loc),
            }
        )
    for row in rows:
        loc = {"lat": row["lat"], "lng": row["lng"]}
        items.append(
            {
                "id": row["id"],
                "title": row["title"],
                "source": "Twoja wioska",
                "category": "inicjatywa",
                "audience": "wszyscy",
                "when": row["when_text"],
                "place": row["place"],
                "blurb": row["blurb"],
                "spots": row["spots"],
                "horizon": "tydzien",
                "art": "park",
                "photo": "/static/img/park.svg",
                "free": True,
                **distance_fields(origin, loc),
            }
        )

    return sorted(
        [enrich_happening(item, joined) for item in items],
        key=lambda e: (0 if e.get("joined") else 1, 0 if e.get("sponsored") else 1, e.get("distance_km") or 0, e.get("when") or ""),
    )


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/qr")
def qr_slide() -> FileResponse:
    return FileResponse(STATIC / "qr.html")


@app.post("/api/village")
def village(query: VillageQuery) -> dict:
    origin = me_origin()
    return {
        "parents": nearby_parents(
            query.want,
            query.similar_age,
            origin=origin,
            radius_km=query.radius_km,
            seeking_filter=query.seeking,
        ),
        "happenings": nearby_happenings(origin),
        "swaps": nearby_swaps(origin),
        "places": nearby_places(origin),
        "want_labels": WANT_LABEL,
        "seeking_labels": SEEKING_LABEL,
    }


@app.post("/api/events")
def create_event(payload: EventIn) -> dict:
    event_id = f"local-{int(time.time() * 1000)}"
    with db() as conn:
        conn.execute(
            """
            INSERT INTO events (id, title, kind, when_text, place, lat, lng, spots, blurb)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_id,
                payload.title.strip(),
                payload.kind,
                payload.when.strip() or "Wkrótce",
                payload.place.strip() or "W Twojej okolicy",
                payload.lat,
                payload.lng,
                8,
                "Dodałaś to w Poznaj wioskę. Sąsiadki w promieniu zobaczą to na liście osiedla.",
            ),
        )
    return {"id": event_id}


@app.post("/api/swaps")
def create_swap(payload: SwapIn) -> dict:
    swap_id = f"swap-{int(time.time() * 1000)}"
    with db() as conn:
        conn.execute(
            """
            INSERT INTO swaps (id, title, platform, url, note, lat, lng, who)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Sylwia')
            """,
            (
                swap_id,
                payload.title.strip(),
                payload.platform,
                payload.url.strip(),
                payload.note.strip() or "Ogłoszenie z Twojej wioski.",
                payload.lat,
                payload.lng,
            ),
        )
    return {"id": swap_id}


@app.post("/api/places")
def create_place(payload: PlaceIn) -> dict:
    place_id = f"place-{int(time.time() * 1000)}"
    kind = payload.kind if payload.kind in PLACE_KIND_LABEL else "miejsce"
    who = (read_profile().get("name") or "Sylwia").strip() or "Sylwia"
    with db() as conn:
        conn.execute(
            """
            INSERT INTO places (id, name, kind, tag, note, lat, lng, who)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                place_id,
                payload.name.strip(),
                kind,
                payload.tag.strip() or PLACE_KIND_LABEL[kind].lower(),
                payload.note.strip() or "Dodane przez wioskę.",
                payload.lat,
                payload.lng,
                who,
            ),
        )
        conn.execute(
            """
            INSERT INTO place_recs (place_id, recommended) VALUES (?, 1)
            ON CONFLICT(place_id) DO UPDATE SET recommended = 1
            """,
            (place_id,),
        )
    return {"id": place_id, "recommended": True}


@app.post("/api/join")
def join(payload: JoinIn) -> dict:
    with db() as conn:
        if payload.joined:
            conn.execute(
                "INSERT OR IGNORE INTO joins (event_id, who) VALUES (?, 'sylwia')",
                (payload.event_id,),
            )
        else:
            conn.execute(
                "DELETE FROM joins WHERE event_id = ? AND who = 'sylwia'",
                (payload.event_id,),
            )
    return {"ok": True, "joined": payload.joined}


@app.get("/api/messages/{parent_id}")
def list_messages(parent_id: str) -> dict:
    with db() as conn:
        rows = conn.execute(
            "SELECT sender, text, at FROM messages WHERE parent_id = ? ORDER BY id",
            (parent_id,),
        ).fetchall()
        conn.execute(
            "INSERT INTO thread_state (parent_id, unread) VALUES (?, 0) ON CONFLICT(parent_id) DO UPDATE SET unread = 0",
            (parent_id,),
        )
    return {"messages": [dict(row) for row in rows], "parent": parent_card(parent_id)}


@app.post("/api/messages")
def send_message(payload: MessageIn) -> dict:
    text = payload.text.strip()
    if not text:
        raise HTTPException(400, "Pusta wiadomość")
    at = time.strftime("%H:%M")
    with db() as conn:
        conn.execute(
            "INSERT INTO messages (parent_id, sender, text, at) VALUES (?, 'ty', ?, ?)",
            (payload.parent_id, text, at),
        )
        reply_text = CHAT_REPLIES.get(payload.parent_id) or "Jasne, daj znać kiedy Ci pasuje."
        reply_at = time.strftime("%H:%M")
        conn.execute(
            "INSERT INTO messages (parent_id, sender, text, at) VALUES (?, ?, ?, ?)",
            (payload.parent_id, payload.parent_id, reply_text, reply_at),
        )
        conn.execute(
            "INSERT INTO thread_state (parent_id, unread) VALUES (?, 0) ON CONFLICT(parent_id) DO UPDATE SET unread = 0",
            (payload.parent_id,),
        )
        rows = conn.execute(
            "SELECT sender, text, at FROM messages WHERE parent_id = ? ORDER BY id",
            (payload.parent_id,),
        ).fetchall()
    return {
        "sender": "ty",
        "text": text,
        "at": at,
        "reply": {"sender": payload.parent_id, "text": reply_text, "at": reply_at},
        "messages": [dict(row) for row in rows],
    }


class KidIn(BaseModel):
    gender: str = "dziecko"
    age_band: str = "6-12m"


class ProfileIn(BaseModel):
    name: str
    district: str = "Podgórze, Kraków"
    district_id: str = "podgorze"
    area_id: str = "stare-podgorze"
    kids: list[KidIn] = []
    interests: list[str] = []
    seeking: list[str] = []
    availability: str = "spacer"
    window: str = ""
    about: str = ""
    quiet: bool = False
    onboarded: bool = False
    email: str = ""
    verified: bool = False
    approx: bool | None = None


class NoticeReadIn(BaseModel):
    notice_id: str


class TrustIn(BaseModel):
    parent_id: str
    met: bool | None = None
    reported: bool | None = None
    starred: bool | None = None


class PlaceRecIn(BaseModel):
    place_id: str
    recommended: bool


def inbox_payload() -> dict:
    with db() as conn:
        rows = conn.execute(
            "SELECT parent_id, sender, text, at FROM messages ORDER BY id"
        ).fetchall()
        unread_rows = conn.execute("SELECT parent_id, unread FROM thread_state").fetchall()
        read_notices = {row["notice_id"] for row in conn.execute("SELECT notice_id FROM notice_read")}
    unread_map = {row["parent_id"]: bool(row["unread"]) for row in unread_rows}
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["parent_id"], []).append(dict(row))
    threads = []
    for parent_id, msgs in grouped.items():
        last = msgs[-1]
        card = parent_card(parent_id)
        threads.append(
            {
                **card,
                "last": last["text"],
                "at": last["at"],
                "unread": unread_map.get(parent_id, last["sender"] != "ty"),
                "count": len(msgs),
            }
        )
    threads.sort(key=lambda t: (0 if t["unread"] else 1, t["at"]), reverse=False)
    threads.sort(key=lambda t: (0 if t["unread"] else 1))
    notices = [{**item, "read": item["id"] in read_notices} for item in NOTICE_SEEDS]
    return {
        "threads": threads,
        "notices": notices,
        "unread_messages": sum(1 for t in threads if t["unread"]),
        "unread_notices": sum(1 for n in notices if not n["read"]),
    }


@app.get("/api/inbox")
def get_inbox() -> dict:
    return inbox_payload()


@app.post("/api/notices/read")
def read_notice(payload: NoticeReadIn) -> dict:
    with db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO notice_read (notice_id) VALUES (?)",
            (payload.notice_id,),
        )
    return inbox_payload()


def read_profile() -> dict:
    with db() as conn:
        row = conn.execute("SELECT payload FROM profile WHERE id = 1").fetchone()
    if not row:
        data = dict(DEFAULT_PROFILE)
    else:
        data = {**DEFAULT_PROFILE, **json.loads(row["payload"])}
    data["kids"] = normalize_kids(data.get("kids"))
    data["seeking"] = normalize_seeking(data.get("seeking"))
    data["district_id"] = data.get("district_id") or "podgorze"
    data["area_id"] = data.get("area_id") or ""
    data["district"] = area_phrase(data["district_id"], data["area_id"])
    data.pop("approx", None)
    if not data.get("availability"):
        data["availability"] = data.get("today") or "spacer"
    return data


@app.get("/api/me")
def get_me() -> dict:
    data = read_profile()
    data.pop("district", None)
    return {
        **data,
        "seeking_options": SEEKING_LABEL,
        "interest_options": INTEREST_LABEL,
        "age_band_options": AGE_BAND_LABEL,
        "gender_options": GENDER_LABEL,
    }


@app.put("/api/me")
def save_me(payload: ProfileIn) -> dict:
    data = payload.model_dump()
    data.pop("approx", None)
    data["kids"] = normalize_kids(data.get("kids"))
    data["seeking"] = normalize_seeking(data.get("seeking"))
    data["district_id"] = data.get("district_id") or "podgorze"
    data["area_id"] = data.get("area_id") or ""
    data["district"] = area_phrase(data["district_id"], data["area_id"])
    with db() as conn:
        conn.execute(
            "INSERT INTO profile (id, payload) VALUES (1, ?) ON CONFLICT(id) DO UPDATE SET payload = excluded.payload",
            (json.dumps(data, ensure_ascii=False),),
        )
    return data


@app.get("/api/trust")
def list_trust() -> dict:
    with db() as conn:
        rows = conn.execute("SELECT parent_id, met, reported, starred FROM trust").fetchall()
    return {
        row["parent_id"]: {
            "met": bool(row["met"]),
            "reported": bool(row["reported"]),
            "starred": bool(row["starred"]),
        }
        for row in rows
    }


@app.post("/api/trust")
def save_trust(payload: TrustIn) -> dict:
    with db() as conn:
        row = conn.execute(
            "SELECT met, reported, starred FROM trust WHERE parent_id = ?",
            (payload.parent_id,),
        ).fetchone()
        met = int(payload.met) if payload.met is not None else (row["met"] if row else 0)
        reported = int(payload.reported) if payload.reported is not None else (row["reported"] if row else 0)
        starred = int(payload.starred) if payload.starred is not None else (row["starred"] if row else 0)
        conn.execute(
            """
            INSERT INTO trust (parent_id, met, reported, starred) VALUES (?, ?, ?, ?)
            ON CONFLICT(parent_id) DO UPDATE SET
                met = excluded.met,
                reported = excluded.reported,
                starred = excluded.starred
            """,
            (payload.parent_id, met, reported, starred),
        )
    return {
        "parent_id": payload.parent_id,
        "met": bool(met),
        "reported": bool(reported),
        "starred": bool(starred),
    }


@app.post("/api/places/recommend")
def save_place_rec(payload: PlaceRecIn) -> dict:
    with db() as conn:
        conn.execute(
            """
            INSERT INTO place_recs (place_id, recommended) VALUES (?, ?)
            ON CONFLICT(place_id) DO UPDATE SET recommended = excluded.recommended
            """,
            (payload.place_id, int(payload.recommended)),
        )
    return {"place_id": payload.place_id, "recommended": payload.recommended}
