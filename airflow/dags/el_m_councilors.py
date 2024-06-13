from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from src.get_meeting_list import main

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

with DAG(
    "extract_n_load_m_councilors_to_BigQuery",
    default_args=default_args,
    schedule_interval="0 0 3 * *",
    catchup=False,
) as dag:

    def generate_m_councilors():
        print("Generated a councilors list.")

    def put_m_councilors():
        print("Put the files of the generated councilors list on a GCS bucket.")

    def load_councilors_files_to_source_table():
        print(
            "Loaded the files of the councilors list into a source table in BigQuery."
        )

    def transform_the_source_table_of_councilors():
        print(
            "Transformed the rows in the source table of councilors and inserted them into the table in the dwh layer."
        )

    def transform_the_dwh_table_of_councilors():
        print(
            "Transformed the rows in the dwh table of councilors and inserted them into the table in the mart layer."
        )

    t_generate_m_councilors = PythonOperator(
        task_id="generate_councilors_list_task", python_callable=generate_m_councilors
    )

    t_put_m_councilors = PythonOperator(
        task_id="put_counsilors_list_task", python_callable=put_m_councilors
    )

    t_load_councilors_lists = PythonOperator(
        task_id="load_coundilors_list_task",
        python_callable=load_councilors_files_to_source_table,
    )

    t_transform_source_councilors = PythonOperator(
        task_id="transform_source_councilors_list_task",
        python_callable=transform_the_source_table_of_councilors,
    )

    t_transform_dwh_councilors = PythonOperator(
        task_id="transform_dwh_councilors",
        python_callable=transform_the_dwh_table_of_councilors,
    )

    (
        t_generate_m_councilors
        >> t_put_m_councilors
        >> t_load_councilors_lists
        >> t_transform_source_councilors
        >> t_transform_dwh_councilors
    )
