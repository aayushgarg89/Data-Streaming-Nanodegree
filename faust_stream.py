"""Defines trends calculations for stations"""
import logging

import faust


logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


# TODO: Define a Faust Stream that ingests data from the Kafka Connect stations topic and
#   places it into a new topic with only the necessary information.
app = faust.App("stations-stream", broker="kafka://localhost:9092", store="memory://")
# TODO: Define the input Kafka Topic. Hint: What topic did Kafka Connect output to?
topic = app.topic("com.cta.station", value_type=Station)
# TODO: Define the output Kafka Topic
out_topic = app.topic("com.cta.station.transformedstation", partitions=1, value_type=TransformedStation)
# TODO: Define a Faust Table
table = app.Table(
    "stations",
    default=str,
    partitions=1,
    changelog_topic=out_topic,
)


#
#
# TODO: Using Faust, transform input `Station` records into `TransformedStation` records. Note that
# "line" is the color of the station. So if the `Station` record has the field `red` set to true,
# then you would set the `line` of the `TransformedStation` record to the string `"red"`
#
#
@app.agent(topic)
def stations(streams):
    for stream in streams:
        transformedstations=TransformedStation(
        station_id=stream.station_id,
        station_name=stream.station_name,
        order=stream.order,
        if stream."red"==True:
            line="red"
        elif stream."blue"==True:
            line="blue"
        else:
            line="green"
        )
        
        await out_topic.send(key=transformedstations.station_id,value=transformedstations)


if __name__ == "__main__":
    app.main()
