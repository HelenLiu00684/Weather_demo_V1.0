import sys

from pathlib import Path


ROOT=Path(

    __file__

).resolve().parent.parent


sys.path.append(

    str(ROOT)

)

import argparse

from sqlalchemy.orm import sessionmaker

from app.database.database import engine

from app.database.reading import WeatherReading

from app.database.event import WeatherEvent


SessionLocal=sessionmaker(

    bind=engine

)

parser=argparse.ArgumentParser()

parser.add_argument(

    "--city",

    required=True

)

args=parser.parse_args()

city=args.city

db=SessionLocal()

readings=db.query(

    WeatherReading

).filter(

    WeatherReading.city==city

).order_by(

    WeatherReading.id.desc()

).limit(

    10

).all()

events=db.query(

    WeatherEvent

).filter(

    WeatherEvent.city==city

).order_by(

    WeatherEvent.id.desc()

).limit(

    20

).all()

print()

print(

    f"City: {city}"

)

print(

    f"Readings Count: {len(readings)}"

)

print(

    f"Event Count: {len(events)}"

)
if readings:

    latest=readings[0]

    print()

    print(

        "Latest Reading"

    )

    print(

        f"Temperature: "

        f"{latest.temperature}C"

    )

    print(

        f"Wind: "

        f"{latest.wind_speed} km/h"

    )

    print(

        f"Weather Code: "

        f"{latest.weather_code}"

    )

event_counter={}

for e in events:

    event_counter[

        e.event_type

    ]=event_counter.get(

        e.event_type,

        0

    )+1


print()

print(

    "Event Summary"

)

for k,v in event_counter.items():

    print(

        f"{k}: {v}"

    )

temps=[

    r.temperature

    for r in readings

]


if temps:

    spread=max(

        temps

    )-min(

        temps

    )

    print()

    print(

        f"Temperature Spread: "

        f"{spread:.1f}C"

    )

print()

print(

    "Risk Summary"

)


if len(events)>=10:

    print(

        "High Event Activity"

    )

elif len(events)>=5:

    print(

        "Moderate Event Activity"

    )

else:

    print(

        "Low Event Activity"

    )    

    print()

print(

    "Investigation Notes"

)


if spread>=10:

    print(

        "Large temperature variation detected"

    )


if "WEATHER_TRANSITION" in event_counter:

    print(

        "Recent weather transitions observed"

    )


if "STRONG_WIND" in event_counter:

    print(

        "Strong wind activity detected"

    )        
