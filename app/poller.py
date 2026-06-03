"""
Weather Polling Pipeline

Responsibilities:

1. Fetch weather data from remote API
2. Store authoritative state in SQLite
3. Prevent duplicate inserts
4. Trigger weather event engine
5. Emit telemetry metrics to InfluxDB
6. Provide continuous monitoring loop
"""

from app.config import CITY_CONFIG

from app.weather_service import fetch_weather

from app.database.reading import get_latest_timestamp

from app.database.reading import create_reading

from app.event_engine import detect_temperature_change

from app.event_engine import detect_strong_wind

from app.event_engine import detect_cross_city_temperature

from app.event_engine import detect_weather_transition

from app.telemetry.metrics import emit_metric

import time

from sqlalchemy.orm import sessionmaker

from app.database.database import engine



SessionLocal=sessionmaker(

    bind=engine

)



def poll_weather(

    db

):

    """
    Execute one polling cycle.

    Flow:

    Weather API
        ↓

    Deduplication
        ↓

    SQLite Storage
        ↓

    Event Engine
        ↓

    Telemetry Emission
    """

    print(

        "poller started"

    )


    #
    # Store city temperatures used for
    # cross-city comparison events
    #

    temperature_snapshot={}


    #
    # Preserve timestamp used by
    # cross-city event generation
    #

    latest_timestamp=None


    for city_name, config in CITY_CONFIG.items():

        try:

            print(

                f"{city_name}: fetching"

            )


            weather=fetch_weather(

                latitude=config["latitude"],

                longitude=config["longitude"]

            )


            print(

                f"{city_name}: fetched"

            )


            current=weather["current"]


            latest_timestamp=current["time"]


            temperature_snapshot[

                city_name

            ]=current[

                "temperature_2m"

            ]


            print(

                f"{city_name}:",

                current["time"]

            )


            latest=get_latest_timestamp(

                db,

                city_name

            )


            duplicate=(

                latest==current["time"]

            )


            #
            # SQLite acts as authoritative storage.
            # Duplicate timestamps are skipped to
            # prevent repeated inserts.
            #

            if duplicate is False:

                create_reading(

                    db=db,

                    city=city_name,

                    timestamp=current["time"],

                    temperature=current["temperature_2m"],

                    apparent_temperature=current["apparent_temperature"],

                    precipitation=current["precipitation"],

                    wind_speed=current["wind_speed_10m"],

                    weather_code=current["weather_code"]

                )


                print(

                    f"{city_name}: reading stored"

                )


            else:

                print(

                    f"{city_name}: telemetry only"

                )


            #
            # Telemetry is observability only.
            # Metrics are emitted regardless of
            # database deduplication.
            #

            emit_metric(

                metric_name=

                    "temperature_celsius",

                value=

                    current[

                        "temperature_2m"

                    ],

                labels={

                    "city":

                        city_name

                }

            )


            emit_metric(

                metric_name=

                    "apparent_temperature",

                value=

                    current[

                        "apparent_temperature"

                    ],

                labels={

                    "city":

                        city_name

                }

            )


            emit_metric(

                metric_name=

                    "wind_speed",

                value=

                    current[

                        "wind_speed_10m"

                    ],

                labels={

                    "city":

                        city_name

                }

            )


            #
            # Execute independent event detectors
            # using current weather state
            #

            detect_temperature_change(

                db=db,

                city=city_name,

                current=current

            )


            detect_strong_wind(

                db=db,

                city=city_name,

                current=current

            )


            detect_weather_transition(

                db=db,

                city=city_name,

                current=current

            )


            print(

                f"{city_name}: complete"

            )


        except Exception as e:

            print(

                f"{city_name}: failed",

                e

            )

            continue


    #
    # Generate cross-city comparison events
    # after all cities are processed
    #

    detect_cross_city_temperature(

        db=db,

        current_data=temperature_snapshot,

        timestamp=latest_timestamp,

        threshold=4

    )


    print(

        "poller finished"

    )



def start_polling_loop():

    """
    Continuous monitoring loop.

    Polling interval can be adjusted
    depending on deployment needs.
    """

    db=SessionLocal()


    while True:

        poll_weather(

            db

        )


        print(

            "poller sleeping..."

        )


        time.sleep(

            30

        )



if __name__=="__main__":

    start_polling_loop()