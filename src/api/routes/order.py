from psycopg2.extras import DictCursor
from database.dbConnect import connectionRead


connection = connectionRead()


def orderGetItem():
    with connection:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""SELECT * FROM public.order;""")
            get_itens = cursor.fetchall()
            cursor.close()
            response_itens = [row_to_dict_order(x) for x in get_itens]
    return response_itens


def row_to_dict_order(row):
    return dict(
        {
            "id": row["id"],
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
        }
    )
