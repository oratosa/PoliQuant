#!/bin/bash

# add PYTHONPATH
export PYTHONPATH=/workspaces/PoliQuant

# Start the Airflow webserver
airflow webserver -p 8080 -D

# Start the Airflow scheduler
airflow scheduler -D

