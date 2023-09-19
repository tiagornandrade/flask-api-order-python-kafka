import os
import psycopg2
from envyaml import EnvYAML


# env = EnvYAML(os.path.abspath("../../../env.yaml"))
env = EnvYAML("../../env.yaml")


def connectionWrite():
    urlWrite = env["DATABASE_URL_1"]
    connectionWrite = psycopg2.connect(urlWrite)
    return connectionWrite


def connectionRead():
    urlRead = env["DATABASE_URL_2"]
    connectionRead = psycopg2.connect(urlRead)
    return connectionRead
