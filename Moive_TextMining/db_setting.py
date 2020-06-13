import pymysql.cursors

def setting():
    conn = pymysql.connect(host='davichiar1.cafe24.com', port=3306, user='davichiar1', passwd='a1b1c1**', db='davichiar1', charset='utf8')
    conn.query("set character_set_connection=utf8;")
    conn.query("set character_set_server=utf8;")
    conn.query("set character_set_client=utf8;")
    conn.query("set character_set_results=utf8;")
    conn.query("set character_set_database=utf8;")
    return conn