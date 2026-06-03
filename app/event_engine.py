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
#
# Rapid Temperature Change Event
#
# Definition:
#
# abs(
#
# current temperature
#
# -
#
# baseline temperature (>12h)
#
# )
#
# >= threshold
#
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
# Strong Wind Event
#
# Definition:
#
# Wind speed exceeds threshold
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
# Cross City Temperature Event
#
# Definition:
#
# max temperature
#
# -
#
# min temperature
#
# >= threshold
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
# Weather Transition Event
#
# Detect transitions between
# weather classifications
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