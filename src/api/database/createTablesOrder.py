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

CREATE_ORDER_DELETED_TABLE = """
    CREATE table if not EXISTS order_deleted (
        id TEXT,
        id_created TEXT,
        name TEXT,
        description TEXT,
        price FLOAT,
        is_deleted BOOLEAN
    );
"""

with connection:
    with connection.cursor() as cursor:
        cursor.execute(CREATE_ORDER_TABLE)
        cursor.execute(CREATE_ORDER_DELETED_TABLE)
