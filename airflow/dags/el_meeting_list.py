from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from src.gcs_connection import GCSConnection
from src.ndl_api import NdlApi

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

with DAG(
    "extract_n_load_meeting_list_to_BigQuery",
    default_args=default_args,
    schedule_interval="0 0 3 * *",
    catchup=False,
) as dag:

    def load_meeting_files_to_source_table():
        print("Loaded the files of the meeting list into a source table in BigQuery.")

    def transform_the_source_table_of_meeting_list():
        print(
            "Transformed the rows in the source table of meeting list and inserted them into the table in the dwh layer."
        )

    def transform_the_dwh_table_of_meeting_list():
        print(
            "Transformed the rows in the dwh table of meeting_list and inserted them into the table in the mart layer."
        )

    # Instantiate the class to pass a method to PythonOperator.
    ndl_api = NdlApi()
    t_extract_meeting_list = PythonOperator(
        task_id="extract_meeting_list_task",
        python_callable=ndl_api.get_meeting_list,
        op_kwargs={
            "start_date": "2022-01-01",
            "end_date": str(datetime.date(datetime.today())),
            "output_dir": "/workspaces/PoliQuant/data/meeting_list",
        },
    )

    # Instantiate the class to pass a method to PythonOperator.
    gcs_conn = GCSConnection()
    t_put_meeting_list = PythonOperator(
        task_id="put_meeting_list_task",
        python_callable=gcs_conn.upload_local_files_to_blob,
        op_kwargs={
            "local_folder_path": "/workspaces/PoliQuant/data/meeting_list",
            "destination_bucket_name": "poliquant",
            "prefix_of_blob_name": "data/input/meeting_list",
        },
    )

    t_load_meeting_lists = PythonOperator(
        task_id="load_meeting_list_task",
        python_callable=load_meeting_files_to_source_table,
    )

    t_transform_source_meeting = PythonOperator(
        task_id="transform_source_meeting_list_task",
        python_callable=transform_the_source_table_of_meeting_list,
    )

    t_transform_dwh_meeting = PythonOperator(
        task_id="transform_dwh_meeting_list_task",
        python_callable=transform_the_dwh_table_of_meeting_list,
    )

    (
        t_extract_meeting_list
        >> t_put_meeting_list
        >> t_load_meeting_lists
        >> t_transform_source_meeting
        >> t_transform_dwh_meeting
    )
