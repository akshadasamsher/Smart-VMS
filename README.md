# Smart Video Management System (Smart VMS)

## 1. Project Overview

Smart VMS is an AI-assisted Video Management System designed for real-time CCTV monitoring, recorded video playback, and automatic intrusion detection.

The system combines a React-based frontend, FastAPI backend, SQLite database, and YOLO-based computer vision model.

The application allows security operators to:

- Monitor live CCTV video
- Play recorded surveillance footage
- Detect people using AI
- Identify intrusion events
- Define a restricted detection zone
- Store detected events in a database
- Display event timestamps
- Display confidence scores
- Monitor camera status
- View recent AI detections
- Monitor active alerts
- Review historical detection events

---

## 2. Main Features

### Live Camera Monitoring

The system displays CCTV video through the web-based VMS interface.

### AI Intrusion Detection

The system uses the YOLO object detection model to identify people in camera footage.

When a person enters the configured restricted area, the system generates an intrusion event.

### Detection Zone

A restricted zone can be configured for the camera.

Only detections occurring inside the configured zone are considered intrusion events.

### Event Management

Each detected event contains:

- Event ID
- Event type
- Camera ID
- Timestamp
- Confidence score
- Detection zone
- Event creation time

### Dashboard

The dashboard provides:

- Camera status
- Active alerts
- Recent AI detections
- Event count
- Camera information
- Detection confidence
- Event timestamps

### Historical Events

All detected events are stored in SQLite and can be retrieved through the backend API.

---

## 3. Technology Stack

### Frontend

- React
- JavaScript
- HTML
- CSS
- Vite

### Backend

- Python
- FastAPI
- Uvicorn

### AI / Computer Vision

- YOLO
- Ultralytics
- OpenCV

### Database

- SQLite

### Communication

- REST API
- HTTP
- JSON

### Development Tools

- Visual Studio Code
- Git
- GitHub
- PowerShell

---

## 4. System Architecture

The Smart VMS follows a three-layer architecture.

```text
                 ┌──────────────────────┐
                 │      CCTV Video      │
                 │   Camera / MP4 File   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   AI Detection       │
                 │ YOLO + OpenCV        │
                 └──────────┬───────────┘
                            │
                   Intrusion Event
                            │
                            ▼
                 ┌──────────────────────┐
                 │    FastAPI Backend   │
                 │    REST API          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     SQLite DB        │
                 │     Events           │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    React Dashboard   │
                 │     Smart VMS UI     │
                 └──────────────────────┘