# API Documentation

## Base URL

http://127.0.0.1:8000

---

## GET /events

Returns all detected events.

### Request

GET /events

### Example Response

[
    {
        "id": 2,
        "event_type": "Intrusion",
        "confidence": 0.94,
        "timestamp": 10.5,
        "camera_id": "Camera 01",
        "zone": "Restricted Area"
    }
]

---

## POST /events

Creates a new detection event.

### Parameters

camera_id  
event_type  
timestamp  
confidence  
zone

### Example

POST /events

camera_id = Camera 01

event_type = Intrusion

timestamp = 10.5

confidence = 0.94

zone = Restricted Area

### Response

The API returns the newly created event.

---

## Example Event

Camera ID:
Camera 01

Event Type:
Intrusion

Timestamp:
10.5 seconds

Confidence:
94%

Zone:
Restricted Area