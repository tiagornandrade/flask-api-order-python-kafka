import psycopg2
from envyaml import EnvYAML


env = EnvYAML('../../env.yaml')

def connection():
    url = env['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection
