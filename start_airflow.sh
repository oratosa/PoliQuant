#!/bin/bash

# Start the Airflow webserver
airflow webserver -p 8080 -D

# Start the Airflow scheduler
airflow scheduler -D

