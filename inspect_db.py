import sqlite3

DB_NAME = 'wakfu_armors.db'

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

for row in c.execute('SELECT id, name, url, type, level, bonuses FROM armors LIMIT 10'):
    print(row)

conn.close()
