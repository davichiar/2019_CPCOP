import pymysql.cursors

def init(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM MV_KEYWORD"
            cursor.execute(sql)
    except:
        pass