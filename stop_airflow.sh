#!/bin/bash

if [ -f $AIRFLOW_HOME/airflow-scheduler.pid ]; then
  kill $(cat $AIRFLOW_HOME/airflow-scheduler.pid)
  rm $AIRFLOW_HOME/airflow-scheduler.pid
fi

if [ -f $AIRFLOW_HOME/airflow-webserver.pid ]; then
  kill $(cat $AIRFLOW_HOME/airflow-webserver.pid)
  rm $AIRFLOW_HOME/airflow-webserver.pid
fi