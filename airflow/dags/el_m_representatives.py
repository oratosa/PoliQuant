from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

from datetime import datetime

from parse_representatives import ParserRepresentatives
from read_sql_file import read_sql_file

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

with DAG(
    "make_dwh_m_representatives_in_BigQuery",
    default_args=default_args,
    schedule_interval="0 0 3 * *",
    catchup=False,
) as dag:

    start = EmptyOperator(
        task_id="start",
    )

    def parse_representatives_list(start=1, end=11):
        for page_number in range(start, end):
            parser = ParserRepresentatives(page_number)
            parser.add_update_date()
            parser.add_members()
            parser.write_csv()

    t_parse_representatives_list = PythonOperator(
        task_id="t_parse_representatives_list",
        python_callable=parse_representatives_list,
    )

    import glob

    SRC_DIR = "/workspaces/PoliQuant/data/politician_list/representatives"
    file_name = "representatives_[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_*.csv"
    path_list = glob.glob(f"{SRC_DIR}/{file_name}")

    t_put_representatives_list = LocalFilesystemToGCSOperator(
        task_id="t_put_representatives_list",
        src=path_list,
        dst="data/input/politician_list/representative/",
        bucket="poliquant",
    )

    sql_load_source_m_representatives = read_sql_file(
        "/workspaces/PoliQuant/sql/load_source_m_representatives.sql"
    )
    t_load_source_m_representatives = BigQueryInsertJobOperator(
        task_id="t_load_source_m_representatives",
        configuration={
            "query": {
                "query": sql_load_source_m_representatives,
                "useLegacySql": False,
            }
        },
        gcp_conn_id="google_cloud_default",
        location="US",
    )

    sql_ctas_dwh_m_representatives = read_sql_file(
        "/workspaces/PoliQuant/sql/ctas_dwh_m_representatives.sql"
    )
    t_ctas_dwh_m_representatives = BigQueryInsertJobOperator(
        task_id="t_ctas_dwh_m_representatives",
        configuration={
            "query": {
                "query": sql_ctas_dwh_m_representatives,
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
        >> t_parse_representatives_list
        >> t_put_representatives_list
        >> t_load_source_m_representatives
        >> t_ctas_dwh_m_representatives
        >> end
    )
