from app.event_engine import detect_weather_transition

from app.database.event import WeatherEvent

from app.database.reading import create_reading



def test_weather_transition(

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

        weather_code=1

    )

    create_reading(

        db=db_session,

        city="Ottawa",

        timestamp="2",

        temperature=10,

        apparent_temperature=10,

        precipitation=0,

        wind_speed=0,

        weather_code=0

    )


    current={

        "weather_code":3,

        "time":"3"

    }


    detect_weather_transition(

        db=db_session,

        city="Ottawa",

        current=current

    )


    events=db_session.query(

        WeatherEvent

    ).all()


    assert len(events)==1

    assert events[0].event_type==(

        "WEATHER_TRANSITION"

    )