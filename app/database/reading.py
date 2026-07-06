from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from sqlalchemy.orm import Session

from datetime import datetime
from datetime import timedelta

from app.database.database import Base


####################################################
#
# Weather Reading ORM Model
#
# Responsibility
#
# Defines the schema of the weather_readings table.
#
# Each WeatherReading object represents one row
# in the SQLite database.
#
# ORM (Object Relational Mapping) allows Python
# objects to be mapped directly to database records.
#
#
####################################################

class WeatherReading(Base):
####################################################
#
# Weather Reading Table Schema
#
# Responsibility
#
# Define the schema of the weather_readings table.
#
# Each WeatherReading object represents one row
# in the SQLite database.
#
# The table stores the authoritative weather
# observations collected by the polling service.
#
#
# Database Row Example
#
# id:                     101
# city:                   "Ottawa"
# timestamp:              "2026-06-08T18:00"
# temperature:            25.8
# apparent_temperature:   27.4
# precipitation:          0.0
# wind_speed:             18.2
# weather_code:           3
#
# One WeatherReading object represents
# one row in the weather_readings table.
# Define an ORM model.
####################################################
    __tablename__ = "weather_readings"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    city = Column(
        String,
        nullable=False
    )

    timestamp = Column(
        String,
        nullable=False
    )

    temperature = Column(
        Float
    )

    apparent_temperature = Column(
        Float
    )

    precipitation = Column(
        Float
    )

    wind_speed = Column(
        Float
    )

    weather_code = Column(
        Integer
    )


####################################################
#
# Create Weather Reading
#
# Persist weather state into
# authoritative storage
# Step 1
# Create ORM Object
#         │
#         ▼
# Step 2
# Add Object to Session
#         │
#         ▼
# Step 3
# Commit Transaction
#         │
#         ▼
# SQLite Database
####################################################

def create_reading(

        db: Session,

        city: str,

        timestamp: str,

        temperature: float,

        apparent_temperature: float,

        precipitation: float,

        wind_speed: float,

        weather_code: int
):
    # Create a WeatherReading ORM object.
    #
    # This object represents one weather observation
    # in memory. It is not persisted to the database
    # until it is added to the session and committed.
    reading = WeatherReading(

        city=city,

        timestamp=timestamp,

        temperature=temperature,

        apparent_temperature=apparent_temperature,

        precipitation=precipitation,

        wind_speed=wind_speed,

        weather_code=weather_code
    )
    # Add the ORM object to the current database session.
    #
    # The object is staged for insertion but has not yet
    # been written to the database.
    db.add(reading)
    # Commit the current transaction and persist
    # the weather observation to SQLite.
    db.commit()

    return reading


####################################################
#
# Retrieve Weather Readings
#
# Supports:
#
# city filtering
#
# result limits
#
####################################################

def get_readings(

        db: Session,

        city: str = None,

        limit: int = 50
):
# Create a query object for the WeatherReading table.
#
# The ORM model (WeatherReading) represents the
# weather_readings database table.
#
# SQL Equivalent:
#
# SELECT *
# FROM weather_readings
    query = db.query(

        WeatherReading

    )

    if city:

        query = query.filter(

            WeatherReading.city == city

        )

    readings = query.order_by(

        WeatherReading.id.desc()

    ).limit(

        limit

    ).all()

    return readings


####################################################
#
# Retrieve Latest Timestamp
#
# Used for duplicate prevention
#
####################################################

def get_latest_timestamp(

        db: Session,

        city: str
):

    latest = db.query(

        WeatherReading

    ).filter(

        WeatherReading.city == city

    ).order_by(

        WeatherReading.id.desc()

    ).first()

    if latest:

        return latest.timestamp

    return None


####################################################
#
# Retrieve Historical Baseline
#
# Used for anomaly detection
#
####################################################

def get_baseline_reading(

        db: Session,

        city: str,

        baseline_hours: int = 12

):

    cutoff = (

        datetime.now()

        -

        timedelta(

            hours=baseline_hours

        )

    ).isoformat()

    baseline = db.query(

        WeatherReading

    ).filter(

        WeatherReading.city == city

    ).filter(

        WeatherReading.timestamp <= cutoff

    ).order_by(

        WeatherReading.timestamp.desc()

    ).first()

    return baseline


####################################################
#
# Retrieve Previous Weather State
#
# Used for transition detection
#
####################################################

def get_previous_weather_code(

        db: Session,

        city: str

):

    reading = db.query(

        WeatherReading

    ).filter(

        WeatherReading.city == city

    ).order_by(

        WeatherReading.id.desc()

    ).offset(

        1

    ).first()

    if reading is None:

        return None

    return reading.weather_code