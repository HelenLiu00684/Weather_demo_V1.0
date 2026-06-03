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
# Weather Reading Table
#
# Purpose:
#
# Store authoritative weather state
#
# This layer owns business state
#
####################################################

class WeatherReading(Base):

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
#
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

    reading = WeatherReading(

        city=city,

        timestamp=timestamp,

        temperature=temperature,

        apparent_temperature=apparent_temperature,

        precipitation=precipitation,

        wind_speed=wind_speed,

        weather_code=weather_code
    )

    db.add(reading)

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