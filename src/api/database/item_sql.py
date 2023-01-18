import os
import psycopg2
from psycopg2.extras import DictCursor


def get_connection():
    url = os.environ.get("DATABASE_URL")
    return psycopg2.connect(url)

def list_item():
    with get_connection:
        with get_connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM items_by_id;")
            get_itens = cursor.fetchall()
            cursor.close()
            response_itens = [row_to_dict(x) for x in get_itens]
    return response_itens

def save_item(item):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO items_by_id (id, name, description, price) VALUES (%s,%s,%s,%s);", (item['id'],item['name'],item['description'], item['price']))
        conn.commit()
        cur.close()

def find_by_name(name):
    with get_connection() as conn:
        cur = conn.cursor(cursor_factory = DictCursor)
        name = '%'+name+'%'
        cur.execute("SELECT * FROM swf_user WHERE name ilike %s", (name,))
        rows = cur.fetchall()
        cur.close()
        data = [row_to_dict(x) for x in rows]
        return data

def delete(uuid):
    with get_connection() as conn:
        cur = conn.cursor()
        print(uuid)
        cur.execute("""DELETE FROM swf_user WHERE id = %s""", (uuid,))
        conn.commit()
        cur.close()

def row_to_dict(row):
    return dict({
        'id' : row['id'],
        'name' : row['name'],
        'email' : row['email'],
        'active' : row['active']
    })