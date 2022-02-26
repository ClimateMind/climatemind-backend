#!/usr/bin/env bash

#wait for the SQL Server to come up
echo "sleeping DB Init script"
sleep 30

echo "running DB init script to start a database in the localhosted mssql server"
python3 ./db-init.py