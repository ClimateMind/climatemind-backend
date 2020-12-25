import pyodbc

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = "tcp:db"
database = "sqldb-web-prod-001"
username = "sa"
password = "Cl1mat3m1nd!"
cnxn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
    + server
    + ";DATABASE="
    + database
    + ";UID="
    + username
    + ";PWD="
    + password,
    autocommit=True,
)
cursor = cnxn.cursor()

# Sample select query
result1 = cursor.execute("SELECT @@version;")
result2 = cursor.execute("SELECT name FROM SYSOBJECTS WHERE xtype='U';")
# result3 = cursor.execute('CREATE DATABASE "sqldb-web-prod-001";')
print(list(result2))

# row = cursor.fetchone()
# while row:
#     print(row[0])
#     row = cursor.fetchone()
