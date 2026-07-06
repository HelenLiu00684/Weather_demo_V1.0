# Weather Monitoring Platform

A production-style weather monitoring platform built with Python.

The platform continuously collects weather observations, stores historical state, detects operational events, exposes REST APIs, exports telemetry, and provides dashboards for observability.

Unlike a simple weather script, this project is designed using layered software architecture and modern backend engineering practices.

---

# Project Goal

Build a monitoring platform capable of:

- Continuously collecting weather observations
- Persisting historical weather state
- Detecting operational weather events
- Providing REST APIs
- Exporting telemetry for observability
- Supporting automated testing and CI

The project demonstrates software engineering practices commonly used in backend monitoring systems.

---

# System Architecture

```
                    Open-Meteo API
                           │
                           ▼
                    Weather Service
                           │
                           ▼
                      Poller Layer
                           │
                           ▼
                SQLite (Authoritative State)
                           │
          ┌────────────────┴───────────────┐
          ▼                                ▼
     Event Engine                     FastAPI
          │                                │
          ▼                                ▼
    Weather Events                  REST Clients
          │
          ▼
    Telemetry Layer
          │
          ▼
       InfluxDB
          │
          ▼
       Grafana
```

---

# Project Structure

```
app/

├── api.py                 # REST API layer
├── poller.py              # Weather collection pipeline
├── weather_service.py     # Open-Meteo client
├── event_engine.py        # Business event detection
├── config.py              # Platform configuration
├── config_influx.py       # Telemetry configuration

├── database/
│   ├── database.py
│   ├── reading.py
│   └── event.py

└── telemetry/
    └── metrics.py


tests/

├── conftest.py
├── test_api.py
├── test_cross_city.py
├── test_deduplication.py
├── test_duplicate.py
├── test_no_temperature_event.py
├── test_strong_wind.py
└── test_weather_transition.py
```

---

# Software Architecture

The platform follows a layered architecture.

## Weather Service

Responsible for:

- Calling the Open-Meteo REST API
- Retrieving current weather observations
- Converting HTTP responses into Python dictionaries

---

## Poller Layer

Responsible for:

- Periodic weather polling
- Multi-city collection
- Timestamp deduplication
- Persisting weather observations
- Invoking the Event Engine
- Emitting telemetry

The Poller acts as the orchestration layer of the platform.

---

## Storage Layer

SQLite serves as the authoritative data source.

Stores:

- Weather readings
- Generated weather events

Responsibilities:

- Historical persistence
- Query support
- State management

---

## Event Engine

The Event Engine converts raw weather observations into operational events.

Current event detectors include:

### Rapid Temperature Change

Detects abnormal temperature changes using historical baseline comparison.

### Strong Wind Detection

Detects significant wind conditions and assigns event severity.

### Weather Transition Detection

Detects changes between weather conditions.

Example:

```
Clear
   ↓
Rain
   ↓
Storm
```

### Cross-City Temperature Detection

Compares temperatures across multiple monitored cities and identifies significant regional differences.

The Event Engine is intentionally separated from the Poller so business rules can evolve independently of data collection.

---

## Telemetry Layer

Telemetry is completely independent from business logic.

Responsibilities:

- Export runtime metrics
- Feed observability dashboards
- Support operational monitoring

Telemetry does **NOT**:

- Modify application state
- Generate business events
- Store weather data

This separation keeps observability independent from application behavior.

---

## API Layer

FastAPI exposes persisted monitoring data through REST APIs.

Available endpoints:

### Health Check

```
GET /health
```

Response:

```json
{
    "status": "ok"
}
```

---

### Weather Readings

```
GET /readings
```

Supports:

- limit
- city filtering

---

### Weather Events

```
GET /events
```

Supports:

- limit
- city filtering

The API layer contains no business logic.
It simply exposes persisted application data.

---

# Testing

The project includes automated unit tests covering:

- REST API validation
- Temperature change detection
- Strong wind detection
- Weather transition detection
- Cross-city temperature detection
- Timestamp deduplication
- Duplicate prevention

Testing is implemented using:

- PyTest
- FastAPI TestClient
- In-memory SQLite

---

# Continuous Integration

GitHub Actions automatically performs:

- Dependency installation
- Test execution
- Validation pipeline

This ensures:

- Clean repository builds
- Repeatable execution
- Continuous verification

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Platform implementation |
| SQLite | Persistent state storage |
| SQLAlchemy | ORM |
| FastAPI | REST API |
| InfluxDB | Telemetry storage |
| Grafana | Dashboard visualization |
| Docker | Containerization |
| PyTest | Automated testing |
| GitHub Actions | Continuous Integration |

---

# Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate:

Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database:

```bash
python create_table.py
```

---

# Running the Platform

Start the weather monitoring platform:

```bash
python run.py
```

Run the REST API independently:

```bash
uvicorn app.api:app --reload
```

---

# Running Tests

```bash
pytest tests -v
```

---

# Docker

Start InfluxDB and Grafana:

```bash
docker compose up
```

---

# Design Philosophy

The platform intentionally separates:

```
Weather Collection

        ↓

State Persistence

        ↓

Business Logic

        ↓

Telemetry

        ↓

Visualization
```

This separation improves:

- Maintainability
- Testability
- Scalability
- Observability

---

# Future Enhancements

Possible future improvements include:

- Alert notification pipeline
- Machine learning based anomaly detection
- Distributed weather collectors
- Prometheus integration
- Kubernetes deployment
- Time-series analytics