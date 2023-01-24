import psycopg2

def connection():
    url = 'postgresql://localhost/market_db'
    connection = psycopg2.connect(url)
    return connection