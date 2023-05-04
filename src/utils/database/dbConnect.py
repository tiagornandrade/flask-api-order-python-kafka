import os
import psycopg2


def connection_write():
    url_write = "postgresql://postgres:postgres@localhost:54321/postgres"
    connection_write = psycopg2.connect(url_write)
    return connection_write


def connection_read():
    url_read = "postgresql://postgres:postgres@localhost:54322/postgres"
    connection_read = psycopg2.connect(url_read)
    return connection_read
