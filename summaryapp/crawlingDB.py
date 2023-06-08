import pymysql

from khj.crawling import get_news

# DB 연결 과정
conn = pymysql.connect(host='127.0.0.1', user='root', password='gkrwls34', db='GOD', charset='utf8')
cur = conn.cursor()

def summary_create():
    # 테이블 생성
    sql = """
        CREATE TABLE summary (
        id int NOT NULL,
        press VARCHAR(10) NOT NULL,
        title VARCHAR(20) NOT NULL,
        category CHAR(10) NOT NULL,
        article VARCHAR(100) NOT NULL,
        datetime VARCHAR(20) NOT NULL,
        link VARCHAR(20)  NOT NULL
        );
    """

    cur.execute(sql)

    cur.execute("SHOW TABLES")

    conn.commit()
    conn.close()
    return

def summary_insert(keyword):
    global conn, cur

    news_df = get_news(keyword)

    try:
        for i in range(0, news_df.shape[0]):
            row = news_df.iloc[i]
            idx = news_df.index[i]
            sql = f'INSERT INTO test VALUES({str(i + 1)}, "{row["press"]}", "{row["title"]}", "{row["category"]}", "{row["article"]}", "{row["datetime"]}", "{row["link"]}")'
            cur.execute(sql)

        conn.commit()
        print(cur.lastrowid)
    finally:
        conn.close()

