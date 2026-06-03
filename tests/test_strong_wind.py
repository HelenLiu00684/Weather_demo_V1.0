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