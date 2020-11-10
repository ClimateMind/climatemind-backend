#wait for the SQL Server to come up
echo "sleeping for mssql server to initialize system databases"
sleep 30
echo "running DB Init script"
/opt/mssql-tools/bin/sqlcmd -S tcp:db -U SA -P Cl1mat3m1nd! -Q "CREATE DATABASE [sqldb-web-prod-001]"
