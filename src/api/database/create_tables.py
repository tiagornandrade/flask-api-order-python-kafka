from database.db_connect import connection


connection = connection()

CREATE_ORDER_TABLE = """
    CREATE table if not EXISTS order_created (
        id TEXT,
        name TEXT,
        description TEXT,
        price FLOAT
    );
"""

CREATE_TRANSACTION_TABLE = """
    CREATE table if not EXISTS transaction_created (
        transaction_id TEXT,
        transaction json
    );
"""

with connection:
    with connection.cursor() as cursor:
        cursor.execute(CREATE_ORDER_TABLE)
        cursor.execute(CREATE_TRANSACTION_TABLE)
