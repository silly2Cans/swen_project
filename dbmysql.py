import pymysql
from pymysql import connect
#give your info for your local machine
conn = connect(host='localhost', port=3306, user='root', passwd='', db='jack')

cur = conn.cursor()

cur.execute("show tables")

print(cur.description)

print()

for row in cur:
   print(row)

conn.commit()

cur.close()
conn.close()