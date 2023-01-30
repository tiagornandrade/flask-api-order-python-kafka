import psycopg2
from envyaml import EnvYAML


env = EnvYAML("../../env.yaml")


def connectionOrder():
    url = env["DATABASE_URL"]
    connection = psycopg2.connect(url)
    return connection


def connectionTransaction():
    urlTransaction = env["DATABASE_URL_2"]
    connectionTransaction = psycopg2.connect(urlTransaction)
    return connectionTransaction
