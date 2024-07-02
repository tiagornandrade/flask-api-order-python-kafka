import os
from apache_beam import Pipeline, Map
from apache_beam.io.kafka import ReadFromKafka
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.jdbc import WriteToJdbc


def process(element):
    return f"Processed: {element}"

def run_pipeline():
    pipeline_options = PipelineOptions()

    with Pipeline(options=pipeline_options) as pipeline:
        kafka_config = {
            "bootstrap.servers": "localhost:9092",
            "group.id": "beam-group"
        }

        kafka_messages = (
            pipeline
            | ReadFromKafka(
                consumer_config=kafka_config,
                topics=["order_created"]
            )
            | Map(process)
            | Map(lambda x: (x,))
            | Map(lambda x: {'value': x})
            | Map(lambda x: (x['value'],))
            .with_output_types(str)
            | WriteToJdbc(
                table_name="orders",
                driver_class_name='org.postgresql.Driver',
                jdbc_url="jdbc:postgresql://localhost:5432/postgres",
                username="postgres",
                password="postgres",
                statement=f"INSERT INTO raw.orders (value) VALUES (?)"
            )
        )

if __name__ == "__main__":
    run_pipeline()
