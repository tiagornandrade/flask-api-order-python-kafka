from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
from pyflink.table.descriptors import Kafka, Json, Schema
from pyflink.table.udf import ScalarFunction
from pyflink.table.window import Tumble


class OrderConsumerFunction(ScalarFunction):
    def eval(self, value):
        print(value)


def create_flink_consumer():
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(env)

    kafka_props = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "flink_consumer_group",
        "auto.offset.reset": "earliest",
    }

    schema = Schema()
    schema.field("user_id", "STRING")
    schema.field("event_key", "STRING")
    schema.field("product_name", "STRING")
    schema.field("description", "STRING")
    schema.field("price", "DOUBLE")
    schema.field("operation", "STRING")

    t_env.connect(
        Kafka()
        .version("universal")
        .topic("order_created")
        .topic("order_deleted")
        .topic("order_updated")
        .properties(kafka_props)
        .start_from_earliest()
        .json_schema(schema)
        .register_schema_as_table("orders")
    )

    t_env.from_path("orders").select("*").to_pandas().apply(
        lambda row: OrderConsumerFunction().eval(row), axis=1
    )

    env.execute("Flink Kafka Consumer")


if __name__ == "__main__":
    create_flink_consumer()
