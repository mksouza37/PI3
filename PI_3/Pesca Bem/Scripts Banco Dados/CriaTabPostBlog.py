import sqlite3
import pandas as pd

connection = sqlite3.connect('site.db')

with open('schema3.sql') as f:
    connection.executescript(f.read())

connection.close()
