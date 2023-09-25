import select
import psycopg2.extensions
import threading
from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'localhost:9092',
}
producer = Producer(conf)


def listen_db_and_send_to_kafka():
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute("LISTEN my_channel;")

    print("Waiting for notifications on channel 'my_channel'")
    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            print("Timeout")
        else:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                print("Got NOTIFY:", notify.payload)
                producer.produce('my_topic', key='db_change', value=notify.payload)
                producer.flush()


if __name__ == '__main__':
    threading.Thread(target=listen_db_and_send_to_kafka, daemon=True).start()
