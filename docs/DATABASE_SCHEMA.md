# Database Schema

## Database

SQLite

## Table: events

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Unique event ID |
| camera_id | TEXT | Camera identifier |
| event_type | TEXT | Type of event |
| timestamp | REAL | Video timestamp |
| confidence | REAL | AI confidence score |
| zone | TEXT | Detection zone |
| created_at | TEXT | Event creation time |

## Example Record

{
    "id": 2,
    "event_type": "Intrusion",
    "confidence": 0.94,
    "timestamp": 10.5,
    "camera_id": "Camera 01",
    "zone": "Restricted Area"
}