from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

from datetime import datetime

from parse_councilors import ParserCouncilors
from read_sql_file import read_sql_file

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

with DAG(
    "make__dwh_m_councilors_in_BigQuery",
    default_args=default_args,
    schedule_interval="0 0 3 * *",
    catchup=False,
) as dag:

    start = EmptyOperator(
        task_id="start",
    )

    def parse_councilors_list(start=207, end=214):
        sessions = range(
            start, end
        )  # 今後の課題: session情報をどこかから取得してくる必要ある。
        for session in sessions:
            councilors = ParserCouncilors(session)
            councilors.add_update_date()
            councilors.add_members()
            councilors.write_csv()

    t_parse_councilors_list = PythonOperator(
        task_id="t_parse_councilors_list",
        python_callable=parse_councilors_list,
    )

    import glob

    SRC_DIR = "/workspaces/PoliQuant/data/politician_list/councilors"
    file_name = "councilors_[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_*.csv"
    path_list = glob.glob(f"{SRC_DIR}/{file_name}")

    t_put_councilors_list = LocalFilesystemToGCSOperator(
        task_id="t_put_councilors_list",
        src=path_list,
        dst="data/input/politician_list/councilors/",
        bucket="poliquant",
    )

    sql_load_source_m_councilors = read_sql_file(
        "/workspaces/PoliQuant/sql/load_source_m_councilors.sql"
    )
    t_load_source_m_councilors = BigQueryInsertJobOperator(
        task_id="t_load_source_m_councilors",
        configuration={
            "query": {
                "query": sql_load_source_m_councilors,
                "useLegacySql": False,
            }
        },
        gcp_conn_id="google_cloud_default",
        location="US",
    )

    sql_ctas_dwh_m_councilors = read_sql_file(
        "/workspaces/PoliQuant/sql/ctas_dwh_m_councilors.sql"
    )
    t_ctas_dwh_m_councilors = BigQueryInsertJobOperator(
        task_id="t_ctas_dwh_m_councilors",
        configuration={
            "query": {
                "query": sql_ctas_dwh_m_councilors,
                "useLegacySql": False,
            }
        },
        gcp_conn_id="google_cloud_default",
        location="US",
    )

    end = EmptyOperator(
        task_id="end",
    )

    (
        start
        >> t_parse_councilors_list
        >> t_put_councilors_list
        >> t_load_source_m_councilors
        >> t_ctas_dwh_m_councilors
        >> end
    )
