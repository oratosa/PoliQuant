from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from src.get_meeting_list import main

default_args = {
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
}

with DAG('extract_data_dag', default_args=default_args, schedule_interval='0 0 3 * *') as dag:
    extract_data_task = PythonOperator(
        task_id='extract_data_task',
        python_callable=main
    )

extract_data_task