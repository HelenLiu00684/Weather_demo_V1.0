####################################################
#
# Telemetry Layer
#
# Responsibility
#
# Convert application metrics into a canonical
# telemetry format and export them to InfluxDB.
#
# Processing Pipeline
#
# Business Logic
#        ↓
# Canonical Metric
#        ↓
# InfluxDB Point
#        ↓
# InfluxDB
#
# Important
#
# - Telemetry is observational only.
# - Telemetry never owns business state.
# - SQLite remains the authoritative data source.
#
####################################################

from influxdb_client import InfluxDBClient

from influxdb_client import Point

from influxdb_client.client.write_api import SYNCHRONOUS

from app.config_influx import *

# --------------------------------------------------------
# InfluxDB Client
#
# Establish a connection to the InfluxDB server.
#
# The client is reused by all telemetry operations
# throughout the application.
# --------------------------------------------------------

client=InfluxDBClient(

    url=INFLUX_URL,

    token=INFLUX_TOKEN,

    org=INFLUX_ORG

)


# --------------------------------------------------------
# InfluxDB Write API
#
# Create a synchronous write interface for exporting
# telemetry metrics to InfluxDB.
#
# SYNCHRONOUS mode ensures that each metric is written
# before the function returns.
# --------------------------------------------------------
write_api=client.write_api(

    write_options=SYNCHRONOUS

)


####################################################
#
# Emit Telemetry Metric
#
# Responsibility
#
# Convert one canonical application metric into
# an InfluxDB Point and export it to InfluxDB.
#
# Input
#
# metric_name : str
#
# Example:
#
# "temperature_celsius"
#
# value : float
#
# Example:
#
# 25.8
#
# labels : Dictionary[str, str]
#
# Example:
#
# {
#     "city": "Ottawa"
# }
#
# Output
#
# InfluxDB Point
#
####################################################
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

# --------------------------------------------------------
# Convert the canonical metric into an InfluxDB Point.
#
# Point Structure:
#
# Measurement
#     ↓
# Field
#     ↓
# Tags
#
# Example:
#
# temperature_celsius
#
# field:
#     value = 25.8
#
# tag:
#     city = Ottawa
# --------------------------------------------------------
    point=Point(

        metric_name

    ).field(

        "value",

        float(value)

    )


# --------------------------------------------------------
# Convert application metadata into InfluxDB tags.
#
# Example:
#
# labels = {
#     "city": "Ottawa"
# }
#
# ↓
#
# city=Ottawa
# --------------------------------------------------------

    for k,v in labels.items():

        point=point.tag(

            k,

            str(v)

        )


# --------------------------------------------------------
# Export the telemetry point to InfluxDB.
#
# Data Flow
#
# Canonical Metric
#        ↓
# InfluxDB Point
#        ↓
# Weather Bucket
#        ↓
# InfluxDB
#
# Canonical Metric
#
# {
#     "metric_name": "temperature_celsius",
#     "value": 25.8,
#     "labels": {
#         "city": "Ottawa"
#     }
# }
#
# ↓
#
# InfluxDB Point
#
# Measurement:
#     temperature_celsius
#
# Field:
#     value = 25.8
#
# Tags:
#     city = Ottawa
#
# --------------------------------------------------------

    write_api.write(

        bucket=INFLUX_BUCKET,

        record=point

    )