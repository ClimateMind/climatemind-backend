#!/usr/bin/env bash

echo "sleeping entrypoint"
sleep 120

# FIXME: unable to run pytest in parallel with xdist plugin due to the error
#  Transaction (Process ID 52) was deadlocked on lock resources with another process and has been chosen as the deadlock victim. Rerun the transaction. (1205) (SQLExecDirectW)')
# pytest -n auto --cipdb

pytest --cipdb