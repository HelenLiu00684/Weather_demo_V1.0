from app.event_engine import detect_cross_city_temperature

from app.database.event import WeatherEvent



def test_cross_city(

        db_session

):

    current_data={

        "Ottawa":10,

        "Toronto":20,

        "Vancouver":12

    }


    detect_cross_city_temperature(

        db=db_session,

        current_data=current_data,

        timestamp="now",

        threshold=5

    )


    events=db_session.query(

        WeatherEvent

    ).all()


    assert len(events)==1

    assert events[0].event_type==(

        "CROSS_CITY_TEMP"

    )