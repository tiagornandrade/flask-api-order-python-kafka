from dbConnect import connectionTransaction


connection2 = connectionTransaction()

CREATE_TRANSACTION_TABLE = """
    CREATE table if not EXISTS transaction_created (
        transaction_id TEXT,
        transaction json
    );
"""

with connection2:
    with connection2.cursor() as cursor2:
        cursor2.execute(CREATE_TRANSACTION_TABLE)
