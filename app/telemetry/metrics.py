"""
Telemetry Layer

Responsibilities:

1. Transform application metrics into
   InfluxDB measurements

2. Attach metadata labels

3. Export observability metrics

Important:

Telemetry is observational only.

Telemetry never owns business state.
"""

from influxdb_client import InfluxDBClient

from influxdb_client import Point

from influxdb_client.client.write_api import SYNCHRONOUS

from app.config_influx import *



client=InfluxDBClient(

    url=INFLUX_URL,

    token=INFLUX_TOKEN,

    org=INFLUX_ORG

)



write_api=client.write_api(

    write_options=SYNCHRONOUS

)



def emit_metric(

        metric_name:str,

        value,

        labels:dict|None=None

):

    """
    Emit one telemetry metric.

    Parameters:

    metric_name:

        Influx measurement name

    value:

        numeric metric value

    labels:

        metadata tags
    """

    labels=labels or {}


    point=Point(

        metric_name

    ).field(

        "value",

        float(value)

    )


    #
    # Convert metadata into tags
    #

    for k,v in labels.items():

        point=point.tag(

            k,

            str(v)

        )


    #
    # Export metric to InfluxDB
    #

    write_api.write(

        bucket=INFLUX_BUCKET,

        record=point

    )