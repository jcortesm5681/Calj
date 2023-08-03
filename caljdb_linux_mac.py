import sqlite  , pandas
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

con = sqlite3.connect("/Users/jac/dist/Festivus.db")

cur = con.cursor()


# Create table
# Insert a row of data


df = pandas.read_csv("https://raw.githubusercontent.com/jcortesm5681/Festivus/main/festivus.ini")
print(df)
df.to_sql("FESTIVUS", con, if_exists='replace', index=False)


# Save (commit) the changes
con.commit()



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
