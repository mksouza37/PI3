import sqlite3

connection = sqlite3.connect('site.db')

with open('schema1A.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
