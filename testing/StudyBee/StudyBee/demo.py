import sqlite3

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
cur.execute("select sql from sqlite_master where type='table' and name='example_table'")
schema = cur.fetchone()
con.close()

entries = [ tmp.strip() for tmp in schema[0].splitlines() if tmp.find("constraint")>=0 or tmp.find("unique")>=0 ]
for i in entries: print(i)