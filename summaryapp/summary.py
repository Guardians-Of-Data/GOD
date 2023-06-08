import pymysql
import pandas as pd


# DB 연결 과정
conn = pymysql.connect(host='127.0.0.1', user='root', password='gkrwls34', db='GOD', charset='utf8')
cur = conn.cursor()

def summary_insert():
    mpg = pd.read_csv('dataset_category.csv')
    mpg['sentence'] = mpg['sentence'].replace('\t','').replace('\n','').replace(" ", "").replace('...','')
    try:
        for i in range(0, mpg.shape[0]):
            row = mpg.iloc[i]
            idx = mpg.index[i]
            sql = f'INSERT INTO summary VALUES({str(i+1)},"{row["sentence"]}","{row["target"]}", "{row["category"]}")'
            cur.execute(sql)

        conn.commit()
        print(cur.lastrowid)
    finally:
        conn.close()

summary_insert()