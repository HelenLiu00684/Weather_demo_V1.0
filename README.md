# Weather Monitoring Platform

A production-style weather monitoring platform built with Python.

This project continuously collects weather observations from the Open-Meteo API, persists historical weather state, detects operational weather events, exposes REST APIs, and exports telemetry for observability.

Unlike a simple weather script, this platform demonstrates modern backend software engineering practices, including layered architecture, event-driven processing, repository abstraction, dependency injection, automated testing, and continuous integration.

---

# Project Goal

The goal of this project is to simulate a real-world monitoring platform rather than a standalone weather application.

The platform demonstrates how monitoring systems typically:

- Collect external observations
- Persist historical operational state
- Detect meaningful events
- Expose monitoring APIs
- Export telemetry
- Support automated testing
- Enable dashboard visualization

The design intentionally separates data collection, business logic, persistence, and observability into independent software layers.

---

# System Architecture

```
                    Open-Meteo API
                           │
                           ▼
                   Weather Service Layer
                           │
                           ▼
                     Poller (Orchestrator)
                           │
                           ▼
               SQLite (Authoritative State)
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
     Event Engine                    REST API Layer
          │                                 │
          ▼                                 ▼
 WeatherEvent Repository              REST Clients
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

# Design Principles

The project follows several software engineering principles commonly used in production monitoring platforms.

## Layered Architecture

Each software component has a clearly defined responsibility.

```
Weather Service
        ↓
Poller
        ↓
Repository
        ↓
Event Engine
        ↓
Telemetry
        ↓
REST API
```

Each layer communicates only with its neighboring layer, improving maintainability and reducing coupling.

---

## Separation of Concerns

Business logic is intentionally separated from:

- Weather collection
- Database persistence
- Telemetry
- REST API exposure

For example:

- The Poller collects observations.
- The Event Engine detects weather events.
- SQLite stores application state.
- Telemetry exports metrics.
- FastAPI exposes persisted data.

Each module performs one responsibility only.

---

## Authoritative State

SQLite serves as the single source of truth for the platform.

The database stores:

- Weather observations
- Generated weather events

Telemetry is intentionally **stateless**.

It never:

- modifies application state
- generates business events
- replaces the database

This design prevents observability code from affecting business behavior.

---

## Event-Driven Processing

Rather than directly responding to weather values, the platform transforms raw observations into operational events.

Current event detectors include:

- Rapid temperature change
- Strong wind
- Weather transition
- Cross-city temperature comparison

This allows higher-level monitoring logic to remain independent from data collection.

---

## Testability

Business logic can be tested independently from:

- REST APIs
- Weather Service
- Telemetry
- Dashboard components

The project includes isolated unit tests using:

- PyTest
- FastAPI TestClient
- In-memory SQLite

This enables deterministic and repeatable testing.

---

# Project Structure

The project follows a layered architecture in which each module has a single responsibility.

```
.
├── README.md                  # Project documentation
├── run.py                     # Platform bootstrap (starts Poller and REST API)
├── create_table.py            # Initialize SQLite database schema
├── docker-compose.yml         # Deploy InfluxDB and Grafana
├── requirements.txt           # Python dependencies
├── weather.db                 # SQLite database (generated)

├── app/
│
│   ├── api.py                 # REST API layer
│   ├── poller.py              # Polling orchestration layer
│   ├── weather_service.py     # Open-Meteo HTTP client
│   ├── event_engine.py        # Business event detection
│   ├── config.py              # City monitoring configuration
│   ├── config_influx.py       # InfluxDB configuration
│   │
│   ├── database/
│   │   ├── database.py        # SQLAlchemy engine and session factory
│   │   ├── reading.py         # WeatherReading repository
│   │   └── event.py           # WeatherEvent repository
│   │
│   └── telemetry/
│       └── metrics.py         # Telemetry metric exporter
│
└── tests/
    ├── conftest.py                # Shared testing fixtures
    ├── test_api.py                # REST API tests
    ├── test_cross_city.py         # Cross-city event tests
    ├── test_deduplication.py      # Duplicate prevention tests
    ├── test_duplicate.py          # Timestamp lookup tests
    ├── test_no_temperature_event.py
    ├── test_strong_wind.py
    └── test_weather_transition.py
```

---

## Layer Responsibilities

### Application Layer

Implements the runtime behavior of the monitoring platform.

Components include:

- Weather data collection
- Event detection
- REST API
- Telemetry export

---

### Repository Layer

Encapsulates all database operations.

Responsibilities include:

- Persist weather observations
- Persist weather events
- Query historical state
- Retrieve baseline observations

The repository layer isolates SQLAlchemy operations from business logic.

---

### Telemetry Layer

Exports runtime metrics to InfluxDB.

Telemetry is intentionally independent from business logic and does not modify application state.

---

### Testing Layer

Provides isolated unit tests for every major subsystem.

Current test coverage includes:

- REST API
- Event Engine
- Repository
- Deduplication
- Cross-city analytics

All tests execute against an in-memory SQLite database.

# Core Components

## Weather Service

The Weather Service is responsible for communicating with the Open-Meteo REST API.

Responsibilities:

- Build HTTP requests
- Retrieve weather observations
- Parse JSON responses
- Return normalized Python dictionaries

The Weather Service contains no business logic.

---

## Poller

The Poller serves as the orchestration layer of the platform.

Responsibilities:

- Poll multiple cities
- Prevent duplicate observations
- Persist weather readings
- Invoke the Event Engine
- Export telemetry

The Poller coordinates platform execution but does not implement event detection logic.

---

## Repository Layer

The Repository Layer provides an abstraction over SQLite.

Responsibilities:

- Persist weather observations
- Persist weather events
- Query historical data
- Retrieve previous weather state

Business logic never communicates directly with SQLAlchemy.

---

## Event Engine

The Event Engine transforms raw observations into higher-level operational events.

Implemented detectors include:

- Rapid Temperature Change
- Strong Wind
- Weather Transition
- Cross-City Temperature Difference

Each detector operates independently, allowing new event types to be added without modifying the Poller.

---

## REST API

FastAPI exposes persisted monitoring data.

Endpoints include:

- GET /health
- GET /readings
- GET /events

The API layer performs read-only operations and contains no business logic.

---

## Telemetry

The Telemetry Layer exports operational metrics to InfluxDB.

Responsibilities:

- Export runtime metrics
- Support dashboard visualization
- Provide platform observability

Telemetry never modifies application state.

# Data Flow

The following diagram illustrates the complete execution flow of the platform.

```
Application Startup

        │

        ▼

run.py

        │

        ├──────────────┐
        ▼              ▼

Poller Thread     FastAPI Server

        │

        ▼

Weather Service

        │

        ▼

Open-Meteo API

        │

        ▼

Current Weather Observation

        │

        ▼

Deduplication

        │

        ▼

WeatherReading Repository

        │

        ▼

SQLite Database
(Authoritative State)

        │

        ▼

Event Engine

        │

        ├──────────────┐
        │              │
        ▼              ▼

Weather Events     Telemetry

        │              │

        ▼              ▼

SQLite         InfluxDB

                       │

                       ▼

                   Grafana
```

---

## Execution Sequence

For every polling cycle, the platform performs the following steps:

### Step 1.

Retrieve weather observations from the Open-Meteo REST API.

---

### Step 2.

Normalize the API response into Python dictionaries.

---

### Step 3.

Compare timestamps with the latest persisted observation.

Duplicate observations are ignored.

---

### Step 4.

Persist new weather observations into SQLite.

SQLite serves as the authoritative application state.

---

### Step 5.

Execute independent event detectors.

Current detectors include:

- Rapid Temperature Change
- Strong Wind
- Weather Transition
- Cross-City Temperature Difference

Each detector evaluates one business rule independently.

---

### Step 6.

Persist generated weather events.

Events are stored separately from raw observations.

---

### Step 7.

Export telemetry metrics.

Telemetry provides observability only.

It never modifies application state.

---

### Step 8.

Expose persisted data through REST APIs.

Clients can retrieve:

- Weather readings
- Weather events

without accessing the internal processing pipeline.

# REST API

The platform exposes read-only monitoring data through FastAPI.

The API layer contains no business logic.

All business processing is completed before requests are served.

---

## GET /health

Verifies that the REST API service is available.

Response

```json
{
    "status":"ok"
}
```

---

## GET /readings

Retrieve persisted weather observations.

### Query Parameters

| Parameter | Description |
|-----------|-------------|
| limit | Maximum number of returned records |
| city | Optional city filter |

Example

```
GET /readings?city=Ottawa&limit=10
```

---

## GET /events

Retrieve generated weather events.

### Query Parameters

| Parameter | Description |
|-----------|-------------|
| limit | Maximum number of returned events |
| city | Optional city filter |

Example

```
GET /events?city=Toronto

```
# Testing

The project includes automated unit tests for every major software component.

## Test Categories

### API Tests

Validate:

- HTTP status codes
- JSON response structure
- REST endpoint behavior

---

### Repository Tests

Validate:

- Database persistence
- Timestamp lookup
- Duplicate prevention

---

### Event Engine Tests

Validate:

- Strong wind detection
- Temperature change detection
- Weather transition detection
- Cross-city comparison

---
# Installation

Create environment:

```bash
python -m venv .venv
```

Activate:

Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create database:

```bash
python create_table.py
```

---

# Running Poller

```bash
python run.py
```

Poller continuously collects weather data.

---

# Running API

```bash
uvicorn app.api:app --reload
```

Open:

```
http://127.0.0.1:8000
```

---

# Running Tests

Execute:

```bash
pytest tests -v
```

Current test coverage includes:

* API validation
* Deduplication
* Event detection
* Cross city logic
* Weather transitions
* Wind detection

---

# Docker

Run:

```bash
docker compose up
```

This starts the platform stack.

---

# CI Pipeline

GitHub Actions automatically runs:

* Dependency installation
* Test execution
* Validation pipeline

CI ensures:

* Clean clone works
* Tests pass automatically
* Submission reproducibility

---

# Technology Choices

| Technology     | Purpose                 |
| -------------- | ----------------------- |
| Python         | Platform implementation |
| SQLite         | Authoritative storage   |
| FastAPI        | API layer               |
| SQLAlchemy     | ORM                     |
| InfluxDB       | Telemetry storage       |
| Grafana        | Visualization           |
| Pytest         | Testing                 |
| GitHub Actions | CI                      |

---

# Cursor Setup

The repository includes:

```
.cursor/
```

Contains:

* Rules
* Agent configuration
* Project-specific workflow settings

This folder is intentionally committed because it is part of the submission requirements.

---

# Engineering Skills Demonstrated

This project demonstrates practical experience with:

- Layered software architecture
- Repository pattern
- Dependency Injection
- SQLAlchemy ORM
- REST API development
- Event-driven processing
- Telemetry and observability
- Automated testing with PyTest
- Docker deployment
- Continuous Integration with GitHub Actions

# Future Enhancements

Potential future improvements include:

- Alert notification service
- Machine learning anomaly detection
- Prometheus integration
- Distributed weather collectors
- Kubernetes deployment
- Time-series analytics
- Historical trend prediction
