####################################################
#
# Weather Monitoring REST API
#
# Responsibility
#
# Expose weather monitoring data through
# RESTful HTTP endpoints.
#
# Available Endpoints
#
# • /health
#      Service health verification
#
# • /readings
#      Retrieve weather observations
#
# • /events
#      Retrieve generated weather events
#
# Dependencies
#
# • FastAPI
#      HTTP request routing
#
# • SQLAlchemy
#      Database session management
#
# • SQLite Repository
#      WeatherReading
#      WeatherEvent
#
# Processing Pipeline
#
# HTTP Request
#        ↓
# FastAPI Router
#        ↓
# Database Query
#        ↓
# ORM Objects
#        ↓
# JSON Response
#
####################################################

from fastapi import FastAPI
from fastapi import Depends

from sqlalchemy.orm import sessionmaker

from app.database.database import engine

from app.database.reading import WeatherReading

from app.database.event import WeatherEvent


app=FastAPI(

    docs_url="/",

    redoc_url=None

)
####################################################
#
# SQLAlchemy Session Factory
#
# Responsibility
#
# Create a session factory for generating
# database sessions.
#
# All sessions created by SessionLocal are
# bound to the configured database engine.
#
# Relationship
#
# Engine
#      ↓
# Session Factory (SessionLocal)
#      ↓
# Database Session (db)
#
####################################################
SessionLocal = sessionmaker(

    #
    # Bind all generated sessions to the
    # configured SQLAlchemy engine.
    #
    bind=engine

)

SessionLocal=sessionmaker(

    bind=engine

)

####################################################
#
# Database Session Dependency
#
# Responsibility
#
# Provide a SQLAlchemy database session
# for each incoming API request.
#
# FastAPI automatically injects this
# dependency into endpoints that declare:
#
#     db = Depends(get_db)
#
# Request Lifecycle
#
# HTTP Request
#        ↓
# Create Database Session
#        ↓
# Execute Database Operations
#        ↓
# Close Database Session
#
####################################################
def get_db():

    db=SessionLocal()

    try:

        yield db

    finally:

        db.close()

####################################################
#
# Health Check Endpoint
#
# Responsibility
#
# Verify that the FastAPI service is running
# and able to accept HTTP requests.
#
# This endpoint does not access the database
# and performs no business logic.
#
# HTTP Request
#
# GET /health
#
# Example Response
#
# {
#     "status": "ok"
# }
#
####################################################
@app.get(

    "/health",

    summary="Health Check"

)

def health():

    return {

        "status":"ok"

    }

####################################################
#
# Retrieve Weather Readings
#
# Responsibility
#
# Query weather observations from the
# WeatherReading repository and expose
# them through the REST API.
#
# Query Parameters
#
# limit
#     Maximum number of returned records.
#
# city
#     Optional city filter.
#
# Dependencies
#
# • Database Session (get_db)
#
# • WeatherReading Repository
#
# Processing Pipeline
#
# HTTP Request
#        ↓
# Receive Query Parameters
#        ↓
# Query SQLite Database
#        ↓
# ORM Objects
#        ↓
# JSON Response
#
####################################################


@app.get(

    "/readings",

    summary="Get Weather Readings",

    description="Retrieve weather readings from database"

)

def get_readings(

        limit:int=20,

        city:str|None=None,

        db=Depends(

            get_db

        )

):
    # --------------------------------------------------------
    # Step 1. Build Database Query
    #
    # Create a SQLAlchemy query for the
    # WeatherReading table.
    #
    # SQL Equivalent:
    #
    # SELECT *
    # FROM weather_readings
    # --------------------------------------------------------

    query=db.query(

        WeatherReading

    )
    # --------------------------------------------------------
    # Step 2. Apply Optional City Filter
    #
    # If a city is specified, restrict the query
    # to weather observations for that city.
    #
    # Example:
    #
    # GET /readings?city=Ottawa
    #
    # SQL Equivalent:
    #
    # WHERE city = 'Ottawa'
    # --------------------------------------------------------


    if city:

        query=query.filter(

            WeatherReading.city==city

        )

    # --------------------------------------------------------
    # Step 3. Execute Database Query
    #
    # Retrieve the newest weather observations.
    #
    # SQL Equivalent:
    #
    # ORDER BY id DESC
    # LIMIT <limit>
    # --------------------------------------------------------
    readings=query.order_by(

        WeatherReading.id.desc()

    ).limit(

        limit

    ).all()

    # --------------------------------------------------------
    # Step 4. Convert ORM Objects to JSON
    #
    # FastAPI cannot directly serialize SQLAlchemy
    # ORM objects. Convert each WeatherReading
    # object into a JSON-serializable dictionary.
    # --------------------------------------------------------
    result=[]


    for r in readings:

        result.append(

            {

                "city":r.city,

                "timestamp":r.timestamp,

                "temperature":r.temperature,

                "wind_speed":r.wind_speed,

                "weather_code":r.weather_code

            }

        )

    # --------------------------------------------------------
    # Step 5. Return JSON Response
    #
    # Response Type:
    #
    # List[Dictionary]
    #
    # Example:
    #
    # [
    #     {
    #         "city":"Ottawa",
    #         "temperature":25.8
    #     }
    # ]
    # --------------------------------------------------------
    return result

####################################################
#
# Retrieve Weather Events
#
# Responsibility
#
# Query generated weather events from the
# WeatherEvent repository and expose them
# through the REST API.
#
# Query Parameters
#
# limit
#     Maximum number of returned events.
#
# city
#     Optional city filter.
#
# Dependencies
#
# • Database Session (get_db)
#
# • WeatherEvent Repository
#
# Processing Pipeline
#
# HTTP Request
#        ↓
# Receive Query Parameters
#        ↓
# Query SQLite Database
#        ↓
# ORM Objects
#        ↓
# JSON Response
#
####################################################

@app.get(

    "/events",

    summary="Get Weather Events",

    description="Retrieve generated weather events"

)

def get_events(

        limit:int=20,

        city:str|None=None,

        db=Depends(

            get_db

        )

):
    # --------------------------------------------------------
    # Step 1. Build Database Query
    #
    # Create a SQLAlchemy query for the
    # WeatherEvent table.
    #
    # SQL Equivalent:
    #
    # SELECT *
    # FROM weather_events
    # --------------------------------------------------------
    query=db.query(

        WeatherEvent

    )

    # --------------------------------------------------------
    # Step 2. Apply Optional City Filter
    #
    # If a city is specified, restrict the query
    # to weather events for that city.
    #
    # Example:
    #
    # GET /events?city=Ottawa
    #
    # SQL Equivalent:
    #
    # WHERE city = 'Ottawa'
    # --------------------------------------------------------
    if city:

        query=query.filter(

            WeatherEvent.city==city

        )
    # --------------------------------------------------------
    # Step 3. Execute Database Query
    #
    # Retrieve the newest generated events.
    #
    # SQL Equivalent:
    #
    # ORDER BY id DESC
    # LIMIT <limit>
    # --------------------------------------------------------

    events=query.order_by(

        WeatherEvent.id.desc()

    ).limit(

        limit

    ).all()

    # --------------------------------------------------------
    # Step 4. Convert ORM Objects to JSON
    #
    # Convert each WeatherEvent ORM object
    # into a JSON-serializable dictionary.
    # --------------------------------------------------------
    result=[]


    for e in events:

        result.append(

            {

                "city":e.city,

                "event_type":e.event_type,

                "severity":e.severity,

                "message":e.message,

                "timestamp":e.timestamp

            }

        )

# --------------------------------------------------------
    # Step 5. Return JSON Response
    #
    # Response Type:
    #
    # List[Dictionary]
    #
    # Example:
    #
    # [
    #     {
    #         "city":"Ottawa",
    #         "event_type":"STRONG_WIND",
    #         "severity":"WARNING",
    #         "message":"wind speed 15.2 km/h",
    #         "timestamp":"2026-07-06T10:00"
    #     }
    # ]
    # --------------------------------------------------------
    return result