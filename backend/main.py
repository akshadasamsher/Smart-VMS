# ============================================================
# SMART VMS - FastAPI Backend
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "vms.db"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Smart VMS API",
    description="Video Management System backend for AI intrusion detection",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def create_database():

    conn = get_connection()

    # Create events table if it doesn't exist
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp REAL NOT NULL,
            camera_id TEXT NOT NULL,
            zone TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


# Create database when application starts
create_database()


# ============================================================
# ROOT API
# ============================================================

@app.get("/")
def root():

    return {
        "message": "SMART VMS BACKEND",
        "status": "running",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "database": str(DATABASE)
    }


# ============================================================
# GET ALL EVENTS
# ============================================================

@app.get("/events")
def get_events():

    conn = get_connection()

    cursor = conn.execute(
        """
        SELECT
            id,
            event_type,
            confidence,
            timestamp,
            camera_id,
            zone
        FROM events
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    events = []

    for row in rows:

        events.append(
            {
                "id": row["id"],
                "event_type": row["event_type"],
                "confidence": row["confidence"],
                "timestamp": row["timestamp"],
                "camera_id": row["camera_id"],
                "zone": row["zone"]
            }
        )

    return events


# ============================================================
# CREATE NEW EVENT
# ============================================================

@app.post("/events")
def create_event(
    camera_id: str,
    event_type: str,
    timestamp: float,
    confidence: float,
    zone: str
):

    # Basic validation
    if not camera_id:
        raise HTTPException(
            status_code=400,
            detail="camera_id is required"
        )

    if not event_type:
        raise HTTPException(
            status_code=400,
            detail="event_type is required"
        )

    if confidence < 0 or confidence > 1:
        raise HTTPException(
            status_code=400,
            detail="confidence must be between 0 and 1"
        )

    if timestamp < 0:
        raise HTTPException(
            status_code=400,
            detail="timestamp cannot be negative"
        )

    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO events
        (
            event_type,
            confidence,
            timestamp,
            camera_id,
            zone
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            event_type,
            confidence,
            timestamp,
            camera_id,
            zone
        )
    )

    conn.commit()

    event_id = cursor.lastrowid

    conn.close()

    # Print event in terminal
    print()
    print("=" * 45)
    print("             EVENT STORED")
    print("=" * 45)
    print(f"ID          : {event_id}")
    print(f"Camera      : {camera_id}")
    print(f"Event Type  : {event_type}")
    print(f"Timestamp   : {timestamp:.2f}")
    print(f"Confidence  : {confidence:.2f}")
    print(f"Zone        : {zone}")
    print("=" * 45)
    print()

    return {
        "success": True,
        "message": "Event stored successfully",
        "id": event_id,
        "camera_id": camera_id,
        "event_type": event_type,
        "timestamp": timestamp,
        "confidence": confidence,
        "zone": zone
    }


# ============================================================
# DELETE ALL EVENTS
# ============================================================

@app.delete("/events")
def delete_events():

    conn = get_connection()

    conn.execute(
        "DELETE FROM events"
    )

    # Reset ID counter
    conn.execute(
        "DELETE FROM sqlite_sequence WHERE name='events'"
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "All events deleted"
    }


# ============================================================
# GET EVENT STATISTICS
# ============================================================

@app.get("/stats")
def get_stats():

    conn = get_connection()

    # Total events
    total_cursor = conn.execute(
        "SELECT COUNT(*) AS count FROM events"
    )

    total_events = total_cursor.fetchone()["count"]

    # Intrusion events
    intrusion_cursor = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM events
        WHERE event_type = 'Intrusion'
        """
    )

    intrusion_events = intrusion_cursor.fetchone()["count"]

    # Average confidence
    confidence_cursor = conn.execute(
        """
        SELECT AVG(confidence) AS average
        FROM events
        """
    )

    average_confidence = confidence_cursor.fetchone()["average"]

    # Cameras with events
    cameras_cursor = conn.execute(
        """
        SELECT COUNT(DISTINCT camera_id) AS count
        FROM events
        """
    )

    active_cameras = cameras_cursor.fetchone()["count"]

    conn.close()

    if average_confidence is None:
        average_confidence = 0

    return {
        "total_events": total_events,
        "intrusion_events": intrusion_events,
        "average_confidence": round(
            average_confidence,
            2
        ),
        "active_cameras": active_cameras
    }


# ============================================================
# STARTUP MESSAGE
# ============================================================

@app.on_event("startup")
def startup_message():

    print()
    print("=" * 45)
    print("             SMART VMS BACKEND")
    print("=" * 45)
    print("API Status : RUNNING")
    print("Database   :", DATABASE)
    print("Events API : http://127.0.0.1:8000/events")
    print("Stats API  : http://127.0.0.1:8000/stats")
    print("=" * 45)
    print()