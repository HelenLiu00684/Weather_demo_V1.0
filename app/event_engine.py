"""
Weather Event Engine

Responsibilities:

1. Detect weather anomalies

2. Generate normalized event records

3. Transform weather state into
   higher level operational events
"""

from app.database.reading import get_baseline_reading

from app.database.reading import get_previous_weather_code

from app.database.event import create_event



####################################################
####################################################
#
# Rapid Temperature Change Event Detector
#
# Dependencies
#
# This detector coordinates two repository modules:
#
# 1. Weather Reading Repository (reading.py)
#
#    Retrieves the historical baseline weather
#    observation used for comparison.
#
# 2. Weather Event Repository (event.py)
#
#    Persists the generated weather event after
#    business rule evaluation.
#
# Processing Pipeline
#
# WeatherReading
#        ↓
# Historical Baseline
#        ↓
# Temperature Comparison
#        ↓
# Event Generation
#        ↓
# WeatherEvent
#
####################################################
####################################################

def detect_temperature_change(

        db,

        city:str,

        current:dict,

        threshold:float=5

):

    """
    Detect rapid temperature changes
    using a historical baseline window.
    """

    baseline=get_baseline_reading(

        db,

        city,

        baseline_hours=12

    )


    #
    # insufficient history
    #

    if baseline is None:

        return


    diff=abs(

        current["temperature_2m"]

        -

        baseline.temperature

    )


    #
    # below event threshold
    #

    if diff < threshold:

        return


    severity="WARNING"


    if diff >=8:

        severity="CRITICAL"


    create_event(

        db=db,

        city=city,

        event_type="RAPID_TEMP_CHANGE",

        severity=severity,

        message=(

            f"temperature changed "

            f"{diff:.1f}C "

            f"within baseline window"

        ),

        timestamp=current["time"]

    )



####################################################
#
# Strong Wind Event Detector
#
# Responsibility
#
# Detect operationally significant wind
# conditions based on predefined thresholds.
#
# Dependencies
#
# 1. Weather Reading
#
#    Input:
#
#    Current Weather Observation
#
#    Example:
#
#    {
#        "wind_speed_10m": 18.2,
#        "time": "2026-06-08T18:00"
#    }
#
# 2. Weather Event Repository (event.py)
#
#    Persist the generated STRONG_WIND
#    event into the weather_events table.
#
# Processing Pipeline
#
# Current Weather State
#          ↓
# Wind Speed Evaluation
#          ↓
# Severity Classification
#          ↓
# Weather Event
#
####################################################

def detect_strong_wind(

        db,

        city:str,

        current:dict

):

    """
    Detect operationally significant
    wind conditions.
    """

    wind=current[

        "wind_speed_10m"

    ]


    if wind <10:

        return


    severity="WARNING"


    if wind >=15:

        severity="HIGH"


    if wind >=20:

        severity="CRITICAL"


    create_event(

        db=db,

        city=city,

        event_type="STRONG_WIND",

        severity=severity,

        message=(

            f"wind speed "

            f"{wind:.1f} km/h"

        ),

        timestamp=current["time"]

    )



####################################################
#
# Cross-City Temperature Event Detector
#
# Responsibility
#
# Compare temperatures across all monitored
# cities and detect abnormal temperature spread.
#
# Dependencies
#
# 1. Polling Layer
#
#    Input:
#
#    Dictionary[str, float]
#
#    Example:
#
#    {
#        "Ottawa": 25.8,
#        "Toronto": 31.2,
#        "Montreal": 24.3
#    }
#
# 2. Weather Event Repository (event.py)
#
#    Persist the generated CROSS_CITY_TEMP
#    event into the weather_events table.
#
# Processing Pipeline
#
# Temperature Snapshot
#          ↓
# Max / Min Comparison
#          ↓
# Temperature Spread
#          ↓
# Severity Classification
#          ↓
# Weather Event
#
####################################################

def detect_cross_city_temperature(

        db,

        current_data:dict,

        timestamp:str,

        threshold:float=5

):

    """
    Compare temperatures across cities
    and generate spread events.
    """

    #
    # requires multiple cities
    #

    if len(current_data) < 2:

        return


    hottest_city=max(

        current_data,

        key=current_data.get

    )


    coldest_city=min(

        current_data,

        key=current_data.get

    )


    max_temp=current_data[

        hottest_city

    ]


    min_temp=current_data[

        coldest_city

    ]


    spread=max_temp-min_temp


    if spread < threshold:

        return


    severity="WARNING"


    if spread >=8:

        severity="HIGH"


    if spread >=12:

        severity="CRITICAL"


    create_event(

        db=db,

        city="ALL",

        event_type="CROSS_CITY_TEMP",

        severity=severity,

        message=(

            f"temperature spread "

            f"{spread:.1f}C "

            f"{hottest_city}"

            f" vs "

            f"{coldest_city}"

        ),

        timestamp=timestamp

    )



####################################################
#
# Weather Transition Event Detector
#
# Responsibility
#
# Detect changes in weather classification
# between consecutive weather observations.
#
# Dependencies
#
# 1. Weather Reading Repository (reading.py)
#
#    Retrieve the previous weather state.
#
# 2. Weather Event Repository (event.py)
#
#    Persist the generated WEATHER_TRANSITION
#    event into the weather_events table.
#
# Processing Pipeline
#
# Previous Weather State
#          ↓
# Current Weather State
#          ↓
# State Comparison
#          ↓
# Weather Transition Event
#
####################################################

def detect_weather_transition(

        db,

        city:str,

        current:dict

):

    """
    Detect weather code changes
    between polling cycles.
    """

    previous_code=get_previous_weather_code(

        db,

        city

    )


    current_code=current[

        "weather_code"

    ]


    #
    # no previous state available
    #

    if previous_code is None:

        return


    #
    # no state transition
    #

    if previous_code == current_code:

        return


    create_event(

        db=db,

        city=city,

        event_type="WEATHER_TRANSITION",

        severity="INFO",

        message=(

            f"weather changed "

            f"{previous_code}"

            f" -> "

            f"{current_code}"

        ),

        timestamp=current["time"]

    )