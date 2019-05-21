
import pg8000

"""
    Args:
        query: string that represents the query to be run

    Returns:
        a tuple of lists where each entry in the tuple represents an entry in the table
        and each item in the list is a column
"""
def run_query(query):
    try:
        connection = pg8000.connect(
        database='bridge_db',
        user='csfire',
        port=5432,
        host='bridge-db.c6xgclrgfvud.us-west-1.rds.amazonaws.com',
        password='thebridge')

        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()
    except pg8000.Error:
        print('Failed to connect to DB')
        return None