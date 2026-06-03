"""
Weather Monitoring API

Responsibilities:

1. Provide health endpoint

2. Expose weather readings

3. Expose generated events

4. Provide query interface for
   monitoring dashboards and users
"""

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


SessionLocal=sessionmaker(

    bind=engine

)


def get_db():

    db=SessionLocal()

    try:

        yield db

    finally:

        db.close()



@app.get(

    "/health",

    summary="Health Check"

)

def health():

    return {

        "status":"ok"

    }



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

    query=db.query(

        WeatherReading

    )


    if city:

        query=query.filter(

            WeatherReading.city==city

        )


    readings=query.order_by(

        WeatherReading.id.desc()

    ).limit(

        limit

    ).all()


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


    return result



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

    query=db.query(

        WeatherEvent

    )


    if city:

        query=query.filter(

            WeatherEvent.city==city

        )


    events=query.order_by(

        WeatherEvent.id.desc()

    ).limit(

        limit

    ).all()


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


    return result