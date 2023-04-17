import os
import psycopg2


def connectionWrite():
    urlWrite = "postgresql://postgres:postgres@localhost:54321/postgres"
    connectionWrite = psycopg2.connect(urlWrite)
    return connectionWrite


def connectionRead():
    urlRead = "postgresql://postgres:postgres@localhost:54322/postgres"
    connectionRead = psycopg2.connect(urlRead)
    return connectionRead
