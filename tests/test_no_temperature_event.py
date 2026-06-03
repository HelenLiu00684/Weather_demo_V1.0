from app.event_engine import detect_temperature_change

from app.database.event import WeatherEvent

from app.database.reading import create_reading



def test_no_temperature_event(

        db_session

):

    create_reading(

        db=db_session,

        city="Ottawa",

        timestamp="1",

        temperature=10,

        apparent_temperature=10,

        precipitation=0,

        wind_speed=0,

        weather_code=0

    )


    current={

        "temperature_2m":12,

        "time":"2"

    }


    detect_temperature_change(

        db=db_session,

        city="Ottawa",

        current=current,

        threshold=5

    )


    events=db_session.query(

        WeatherEvent

    ).all()


    assert len(events)==0