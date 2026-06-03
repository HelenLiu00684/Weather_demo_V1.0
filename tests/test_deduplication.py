from app.database.reading import create_reading

from app.database.reading import get_latest_timestamp

from app.database.reading import WeatherReading



def test_duplicate_prevention(

        db_session

):

    timestamp="same_time"


    create_reading(

        db=db_session,

        city="Ottawa",

        timestamp=timestamp,

        temperature=10,

        apparent_temperature=10,

        precipitation=0,

        wind_speed=5,

        weather_code=0

    )


    latest=get_latest_timestamp(

        db_session,

        "Ottawa"

    )


    duplicate=(

        latest==timestamp

    )


    if duplicate is False:

        create_reading(

            db=db_session,

            city="Ottawa",

            timestamp=timestamp,

            temperature=10,

            apparent_temperature=10,

            precipitation=0,

            wind_speed=5,

            weather_code=0

        )


    count=db_session.query(

        WeatherReading

    ).count()


    assert count==1