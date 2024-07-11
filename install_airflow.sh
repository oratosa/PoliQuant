#!/bin/bash
export AIRFLOW_HOME=${PWD}/airflow
echo "export AIRFLOW_HOME=$AIRFLOW_HOME" >> ~/.bashrc
echo "Airflow home is set to: $AIRFLOW_HOME"

export AIRFLOW_VERSION=2.9.1
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
echo "This script will install Airflow version $AIRFLOW_VERSION, with Python $PYTHON_VERSION."

sleep 3

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
pip install "apache-airflow==${AIRFLOW_VERSION}" apache-airflow[google]
pip install "apache-airflow==${AIRFLOW_VERSION}" apache-airflow-providers-openlineage[common.sql]