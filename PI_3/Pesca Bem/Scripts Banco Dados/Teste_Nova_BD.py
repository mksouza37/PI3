import sqlite3


conn = sqlite3.connect('site.db')
#conn.row_factory = sqlite3.Row


#consulta = conn.execute('SELECT * FROM Postblog').fetchall()
#print("b",conn.execute('SELECT * FROM empresas').fetchall())
#consulta = conn.execute('SELECT * FROM User').fetchall()

cursor = conn.cursor()
sql_delete_query ="""DELETE FROM Post WHERE title='My First Update Post'"""
cursor.execute(sql_delete_query)
conn.commit()
cursor.close()


#for item in consulta:
#    print(item[1:5])

conn.close()
