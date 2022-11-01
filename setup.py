import sqlite3

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()
conn.execute("CREATE TABLE userdata(id INTEGER PRIMARY KEY, username TEXT, diamond INTEGER, gold INTEGER, exp INTEGER, registerAt INTEGER)")
conn.commit()
conn.close()