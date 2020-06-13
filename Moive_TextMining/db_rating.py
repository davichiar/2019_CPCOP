def init(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM MV_RATING"
            cursor.execute(sql)
    except:
        pass

def insert(conn, id, rating1, rating2, rating3):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO MV_RATING VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id, rating1, rating2, rating3))
    except:
        pass