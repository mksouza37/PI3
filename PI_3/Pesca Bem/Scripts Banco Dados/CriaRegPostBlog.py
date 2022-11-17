import sqlite3
from datetime import datetime

now = datetime.now()
connection = sqlite3.connect('site.db')


cur = connection.cursor()

cur.execute("INSERT INTO Postblog (id, title, date_posted, content, user_id) VALUES (?,?,?,?,?)",
                (1, "b", '2007-01-01 10:00:00', "c", 1)

            
                )

connection.commit()
connection.close()

#(1, "b", now.strftime("%d/%m/%Y %H:%M:%S"), "c", 1)
