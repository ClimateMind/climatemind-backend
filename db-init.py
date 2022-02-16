import pymssql

print('db-init.py started.')
connection = pymssql.connect("tcp:db", "SA", "Cl1mat3m1nd!", "tempdb")
connection.autocommit(True)
cursor = connection.cursor()
cursor.execute("""CREATE DATABASE [sqldb-web-prod-001]""")
connection.autocommit(False)
