#!/usr/bin/env bash

#wait for the SQL Server to come up
echo "sleeping DB Init script"
sleep 30

echo "running DB init script to start a database in the localhosted mssql server"
/opt/mssql-tools/bin/sqlcmd -S tcp:db -U SA -P Cl1mat3m1nd! -Q "CREATE DATABASE [sqldb-web-prod-001]"