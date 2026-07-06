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

# --------------------------------------------------------
# Build HTTP Request Parameters
#
# Data Structure:
#
# Dictionary[str, Any]
#
# Example:
#
# {
#     "latitude": 45.42,
#     "longitude": -75.69,
#     "current": [
#         "temperature_2m",
#         "apparent_temperature",
#         "precipitation",
#         "wind_speed_10m",
#         "weather_code"
#     ],
#     "wind_speed_unit": "kmh",
#     "timezone": "auto"
# }
#
# These parameters are automatically encoded as
# URL query parameters by the Requests library.
#
# Example HTTP Request:
#
# GET /v1/forecast?
# latitude=45.42&
# longitude=-75.69&
# current=temperature_2m,apparent_temperature,
#         precipitation,wind_speed_10m,weather_code&
# wind_speed_unit=kmh&
# timezone=auto
# --------------------------------------------------------


    params={

        "latitude":latitude,

        "longitude":longitude,
    # Weather variables requested from
    # the Open-Meteo API.
    #
    # Data Structure:
    #
    # List[str]
    #
    # Each element specifies one weather
    # measurement to be returned in the
    # "current" section of the API response.
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