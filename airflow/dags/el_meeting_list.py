from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

from datetime import datetime

from src.gcs_connection import GCSConnection
from src.ndl_api import NdlApi
from src.read_sql_file import read_sql_file

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

with DAG(
    "make_dwh_meeting_list_in_BigQuery",
    default_args=default_args,
    schedule_interval="0 0 3 * *",
    catchup=False,
) as dag:

    # Instantiate the class to pass a method to PythonOperator.
    ndl_api = NdlApi()
    t_extract_meeting_list = PythonOperator(
        task_id="t_extract_meeting_list",
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
        task_id="t_put_meeting_list",
        python_callable=gcs_conn.upload_local_files_to_blob,
        op_kwargs={
            "local_folder_path": "/workspaces/PoliQuant/data/meeting_list",
            "destination_bucket_name": "poliquant",
            "prefix_of_blob_name": "data/input/meeting_list",
        },
    )

    sql_load_source_meeting_list = read_sql_file(
        "/workspaces/PoliQuant/sql/load_source_meeting_list.sql"
    )
    t_load_source_meeting_lists = BigQueryInsertJobOperator(
        task_id="t_load_source_meeting_list",
        configuration={
            "query": {
                "query": sql_load_source_meeting_list,
                "useLegacySql": False,
            }
        },
        gcp_conn_id="google_cloud_default",
        location="US",
    )

    sql_insert_dwh_meeting_list = read_sql_file(
        "/workspaces/PoliQuant/sql/insert_dwh_meeting_list.sql"
    )
    t_insert_dwh_meeting_list = BigQueryInsertJobOperator(
        task_id="t_insert_dwh_meeting_list",
        configuration={
            "query": {
                "query": sql_insert_dwh_meeting_list,
                "useLegacySql": False,
            }
        },
        gcp_conn_id="google_cloud_default",
        location="US",
    )

    # The following task will be separated to another dag file to make the tables in the mart layer.
    # sql_ctas_mart_meeting_list = read_sql_file(
    #     "/workspaces/PoliQuant/sql/ctas_mart_meeting_list.sql"
    # )
    # t_ctas_mart_meeting_list = BigQueryInsertJobOperator(
    #     task_id="t_ctas_mart_meeting_list",
    #     configuration={
    #         "query": {
    #             "query": sql_ctas_mart_meeting_list,
    #             "useLegacySql": False,
    #         }
    #     },
    #     gcp_conn_id="google_cloud_default",
    #     location="US",
    # )

    (
        t_extract_meeting_list
        >> t_put_meeting_list
        >> t_load_source_meeting_lists
        >> t_insert_dwh_meeting_list
    )
