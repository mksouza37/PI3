import sqlite3
import pandas as pd

connection = sqlite3.connect('site.db')

with open('schema4.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

df = pd.read_excel (r'C:\Users\Markus\Documents\Web Projects\PI_2\Pesca Bem\Portal\flaskblog\Legislacao_2022.xlsx', sheet_name='Planilha1')
print(df)

a=[]
b=[]

for lin in range(0,len(df)):

    a.append(int(df.iloc[lin,0]))
    b.append(int(df.iloc[lin,2]))

for lin in range(0,len(df)):

    cur.execute("INSERT INTO Legislacao (ident, siglaTipo, ano, ementa, uri) VALUES (?,?,?,?,?)",
                (a[lin], df.iloc[lin,1], b[lin], df.iloc[lin,3], df.iloc[lin,4])
                )
    
cur.execute('''SELECT * from Legislacao''')
print(cur.fetchall())
print(cur.lastrowid)

connection.commit()
connection.close()
