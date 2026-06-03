# Weather Monitoring Platform

## Overview

This project is a weather monitoring platform designed to continuously collect weather data, store historical records, detect meaningful events, expose APIs, and provide observability through telemetry and dashboards.

Unlike a simple weather script, this platform focuses on:

* Automated polling
* Historical storage
* Event detection
* API exposure
* Observability
* Monitoring workflows
* Automated testing and CI

The system continuously polls multiple cities and transforms raw weather readings into higher-level weather events.

---

# Architecture

```
Open-Meteo API

        ↓

Poller Layer

        ↓

SQLite Database
(authoritative state)

        ↓

Event Engine

        ↓

Weather Events DB

        ↓

Telemetry Layer

        ↓

InfluxDB

        ↓

Grafana Dashboard

        ↓

FastAPI

        ↓

Users / Dashboards / Queries
```

---

# Project Structure

```
app/

├── api.py

├── poller.py

├── weather_service.py

├── event_engine.py

├── config.py

├── config_influx.py

├── database/

│   ├── database.py

│   ├── reading.py

│   └── event.py

└── telemetry/

    └── metrics.py


tests/

├── test_api.py

├── test_cross_city.py

├── test_deduplication.py

├── test_duplicate.py

├── test_no_temperature_event.py

├── test_strong_wind.py

└── test_weather_transition.py
```

---

# Core Components

## Poller Layer

Responsibilities:

* Poll Open-Meteo API
* Support multiple cities
* Deduplicate repeated timestamps
* Store readings into database

---

## Storage Layer

SQLite acts as the authoritative state.

Stores:

* Weather readings
* Weather events

SQLite was selected because:

* Lightweight
* Easy deployment
* Simple local development
* Suitable for historical records

---

## Event Engine

Transforms raw weather readings into higher-level events.

Current event types:

### Temperature Change Detection

Detects significant temperature variations.

Purpose:

* Detect abnormal temperature shifts
* Reduce noise from small fluctuations

---

### Strong Wind Detection

Detects strong wind conditions.

Purpose:

* Identify severe weather conditions
* Generate operational alerts

---

### Weather Transition Detection

Detects weather code transitions.

Example:

```
Clear

↓

Rain

↓

Storm
```

Purpose:

* Detect meaningful weather changes

---

### Cross City Temperature Detection

Compares cities.

Purpose:

* Detect abnormal regional differences
* Demonstrate multi-city analytics

---

# Telemetry Layer

Telemetry is intentionally separated from business logic.

Responsibilities:

* Emit metrics
* Export observability data
* Feed dashboards

Telemetry does NOT:

* Own state
* Modify state
* Make decisions

This separation prevents observability code from affecting platform behavior.

---

# API Layer

FastAPI exposes monitoring data.

Endpoints:

## Health Check

```
GET /health
```

Returns:

```
{

"status":"ok"

}
```

---

## Weather Readings

```
GET /readings
```

Supports:

* limit
* city filtering

---

## Weather Events

```
GET /events
```

Supports:

* limit
* city filtering

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

# Design Philosophy

This project intentionally separates:

```
Business Logic

↓

Telemetry

↓

Observability
```

Goals:

* Reproducibility
* Maintainability
* Testability
* Monitoring-first design

The platform is designed as a monitoring system rather than a simple weather script.
