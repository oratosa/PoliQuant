#!/bin/bash

# Set PYTHONPATH
export PYTHONPATH=/workspaces/PoliQuant

# Set the key file path of GCP authentification
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/secrets/gcp-service-account-key.json"

# Start the Airflow webserver
airflow webserver -p 8080 -D

# Start the Airflow scheduler
airflow scheduler -D

