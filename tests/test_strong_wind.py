####################################################
#
# Strong Wind Event Unit Test
#
# Responsibility
#
# Verify that the Event Engine generates
# a STRONG_WIND event when the wind speed
# exceeds the configured threshold.
#
# Validation
#
# • Event is generated
#
# • Event type is correct
#
# • Severity level is correct
#
# Processing Pipeline
#
# Build Weather State
#          ↓
# Execute Strong Wind Detector
#          ↓
# Query WeatherEvent Table
#          ↓
# Validate Generated Event
#
####################################################
from app.event_engine import detect_strong_wind

from app.database.event import WeatherEvent



def test_strong_wind_event(

        db_session

):

    current={

        "wind_speed_10m":18,

        "time":"2026"

    }


    detect_strong_wind(

        db=db_session,

        city="Ottawa",

        current=current

    )


    events=db_session.query(

        WeatherEvent

    ).all()


    assert len(

        events

    )==1


    assert events[0].event_type=="STRONG_WIND"


    assert events[0].severity=="HIGH"