import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

cursor.execute("SELECT * FROM nfc_project WHERE column_name LIKE '%nfc_project%'")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()