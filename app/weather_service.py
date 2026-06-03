import requests


####################################################
#
# Weather Service Layer
#
# Responsibilities:
#
# Retrieve weather data
#
# Convert remote API response
#
# Return parsed weather state
#
####################################################


####################################################
#
# Retrieve weather data from
#
# Open-Meteo API
#
# Pipeline:
#
# API
#
# ↓
#
# JSON Response
#
# ↓
#
# Python Dictionary
#
####################################################

def fetch_weather(

        latitude: float,

        longitude: float

):

    url="https://api.open-meteo.com/v1/forecast"


    params={

        "latitude":latitude,

        "longitude":longitude,

        "current":[

            "temperature_2m",

            "apparent_temperature",

            "precipitation",

            "wind_speed_10m",

            "weather_code"

        ],

        "wind_speed_unit":"kmh",

        "timezone":"auto"

    }


    response=requests.get(

        url,

        params=params,

        timeout=20

    )


    return response.json()