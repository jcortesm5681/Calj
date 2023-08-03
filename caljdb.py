import sqlite3  , pandas
###
#Este programa carga en la base de datos sqlite los festivos de colombia que estan almacenados en la ruta del archivo plano en GITHUB
#"https://raw.githubusercontent.com/jcortesm5681/Festivus/main/festivus.ini"
# usa la libreria PANDAS para cargar facilmente de CSV a la BD dicha.

## selecconar ruta del archivo donde se va a guardar la BD, tiene que ser el mismo que en calj sinux o max puede ser 

con = sqlite3.connect("D:/dist/Festivus.db") # rutas en windows
cur = con.cursor()

# Create table
# Insert a row of data
df = pandas.read_csv("https://raw.githubusercontent.com/jcortesm5681/Festivus/main/festivus.ini")
df.to_sql("FESTIVUS", con, if_exists='replace', index=False,method="multi")
# Save (commit) the changes
con.commit()
# validar si el contenido en la BD quedó bien guardado. 
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cur.fetchall())
cur.execute("select FEST from FESTIVUS")
print(cur.fetchall())

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()


#para compilar y probar se usa:
#C:\Users\JAC\AppData\Local\Programs\Python\Python311\python D:\dist\caljdb.py 
#
#para volverlo ejecutable:
#pyinstaller --onefile D:\Usuario\Downloads\calj2.py

# si jode por:   ImportError: No module named _bootlocale
# usar:
# pyinstaller --exclude-module _bootlocale --onefile  calj2.py
