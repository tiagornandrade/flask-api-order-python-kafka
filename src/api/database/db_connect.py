import psycopg2


def connection():
    url = "postgresql://postgres:postgres@localhost:54321/postgres"
    connection = psycopg2.connect(url)
    return connection
