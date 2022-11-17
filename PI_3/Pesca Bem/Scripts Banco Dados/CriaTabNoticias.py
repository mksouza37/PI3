import sqlite3
import pandas as pd

connection = sqlite3.connect('site.db')

with open('schema5.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

df = pd.read_excel (r'C:\Users\Markus\Desktop\Materiais - Curso\Bimestre 9\P Integrador\Lista Noticias.xlsx', sheet_name='Planilha1')

for lin in range(0,len(df)):

    cur.execute("INSERT INTO Noticias (dataPub, titulo, link) VALUES (?,?,?)",
                (df.iloc[lin,0], df.iloc[lin,1], df.iloc[lin,2])
                )

connection.commit()
connection.close()
