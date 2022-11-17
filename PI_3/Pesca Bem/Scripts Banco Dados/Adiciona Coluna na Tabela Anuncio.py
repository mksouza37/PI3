import sqlite3


dbCon = sqlite3.connect("site.db")
cur   = dbCon.cursor()

addColumn = "ALTER TABLE anuncio ADD COLUMN nomeAnunciante TEXT"

cur.execute(addColumn)

masterQuery = "select * from sqlite_master"

cur.execute(masterQuery)

tableList = cur.fetchall()

for table in tableList:

    print("Database Object Type: %s"%(table[0]))

    print("Database Object Name: %s"%(table[1]))

    print("Table Name: %s"%(table[2]))

    print("Root page: %s"%(table[3]))

    print("**SQL Statement**: %s"%(table[4]))


dbCon.close()
