from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Session

from app.database.database import Base


#####################################################
#
# Weather Event Table
#
# Purpose:
#
# Store normalized event records.
# Events represent operational observations,
# not raw weather readings.
#
#####################################################


class WeatherEvent(Base):

    __tablename__ = "weather_events"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    city = Column(
        String,
        nullable=False
    )

    event_type = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    timestamp = Column(
        String,
        nullable=False
    )


##################################################
#
# Create Event
#
# Duplicate suppression prevents repeated event
# generation for the same city, event type,
# and timestamp.
#
##################################################


def create_event(
        db: Session,
        city: str,
        event_type: str,
        severity: str,
        message: str,
        timestamp: str
):

    if event_exists(
            db,
            city,
            event_type,
            timestamp
    ):
        return

    event = WeatherEvent(
        city=city,
        event_type=event_type,
        severity=severity,
        message=message,
        timestamp=timestamp
    )

    db.add(event)
    db.commit()

    return event


##################################################
#
# Read Events
#
# Return newest generated events first.
#
##################################################


def get_events(
        db: Session,
        limit: int = 50
):

    events = db.query(
        WeatherEvent
    ).order_by(
        WeatherEvent.id.desc()
    ).limit(
        limit
    ).all()

    return events


##################################################
#
# Duplicate Event Detection
#
##################################################


def event_exists(
        db: Session,
        city: str,
        event_type: str,
        timestamp: str
):

    existing = db.query(
        WeatherEvent
    ).filter(
        WeatherEvent.city == city
    ).filter(
        WeatherEvent.event_type == event_type
    ).filter(
        WeatherEvent.timestamp == timestamp
    ).first()

    return existing is not None