import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.kafka import ReadFromKafka
from apache_beam.io.kafka import WriteToKafka


def run_pipeline():
    pipeline_options = PipelineOptions(
        runner="DirectRunner",
        streaming=True,
    )

    with beam.Pipeline(options=pipeline_options) as pipeline:
        kafka_config = {
            "bootstrap.servers": "localhost:9092",
            "group.id": "beam-group",
            "auto.offset.reset": "earliest"
        }

        read_kafka = (
            pipeline
            | "ReadFromKafka" >> ReadFromKafka(
                consumer_config=kafka_config,
                topics=["order_created"]
            )
        )

        write_kafka = (
            read_kafka
            | "WriteToKafka" >> WriteToKafka(
                producer_config={"bootstrap.servers": "localhost:9092"},
                topic="processed_orders",
            )
        )

        result = pipeline.run()
        result.wait_until_finish()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run_pipeline()
