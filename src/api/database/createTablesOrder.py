from dbConnect import connectionOrder


connection = connectionOrder()

CREATE_ORDER_TABLE = """
    CREATE table if not EXISTS order_created (
        id TEXT,
        name TEXT,
        description TEXT,
        price FLOAT
    );
"""

with connection:
    with connection.cursor() as cursor:
        cursor.execute(CREATE_ORDER_TABLE)
