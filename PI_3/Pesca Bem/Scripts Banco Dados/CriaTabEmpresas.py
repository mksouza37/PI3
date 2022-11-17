import sqlite3
import pandas as pd

connection = sqlite3.connect('site.db')

with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

df = pd.read_excel (r'C:\Users\Markus\Desktop\Materiais - Curso\Bimestre 9\P Integrador\Lista 500 Empresas - Certificado Ambiental.xlsx', sheet_name='base')

for lin in range(0,len(df)):

    cur.execute("INSERT INTO empresas (nome, cnpj, cidade, estado, ramo, conduta) VALUES (?,?,?,?,?,?)",
                (df.iloc[lin,0], df.iloc[lin,1], df.iloc[lin,2], df.iloc[lin,3], df.iloc[lin,4], df.iloc[lin,5])
                )

connection.commit()
connection.close()
