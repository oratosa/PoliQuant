from airflow.models.dag import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)

from datetime import datetime
import glob

from ndl_api import NdlApi
from parse_councilors import ParserCouncilors
from parse_representatives import ParserRepresentatives
from read_sql_file import read_sql_file

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

with DAG(
    "make_mart_tables",
    default_args=default_args,
    schedule_interval="0 0 3 * *",
    catchup=False,
) as dag:

    start = EmptyOperator(
        task_id="start",
    )

    with TaskGroup(group_id="g_meeting_list") as g_meeting_list:
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

        SRC_DIR_MEETING_LIST = "/workspaces/PoliQuant/data/meeting_list"
        file_name_meeting_list = (
            "meeting_list_[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_*.json"
        )
        path_list_meeting_list = glob.glob(
            f"{SRC_DIR_MEETING_LIST}/{file_name_meeting_list}"
        )

        t_put_meeting_list = LocalFilesystemToGCSOperator(
            task_id="t_put_meeting_list",
            src=path_list_meeting_list,
            dst="data/input/meeting_list/",
            bucket="poliquant",
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

        (
            t_extract_meeting_list
            >> t_put_meeting_list
            >> t_load_source_meeting_lists
            >> t_insert_dwh_meeting_list
        )

    with TaskGroup(group_id="g_councilors") as g_councilors:

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

        SRC_DIR_COUNCILORS = "/workspaces/PoliQuant/data/politician_list/councilors"
        file_name_councilors = (
            "councilors_[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_*.csv"
        )
        path_list_councilors = glob.glob(f"{SRC_DIR_COUNCILORS}/{file_name_councilors}")

        t_put_councilors_list = LocalFilesystemToGCSOperator(
            task_id="t_put_councilors_list",
            src=path_list_councilors,
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

        (
            t_parse_councilors_list
            >> t_put_councilors_list
            >> t_load_source_m_councilors
            >> t_ctas_dwh_m_councilors
        )

    with TaskGroup(group_id="g_representatives") as g_representatives:

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

        SRC_DIR_REPRESENTATIVES = (
            "/workspaces/PoliQuant/data/politician_list/representatives"
        )
        file_name_representatives = (
            "representatives_[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_*.csv"
        )
        path_list_representatives = glob.glob(
            f"{SRC_DIR_REPRESENTATIVES}/{file_name_representatives}"
        )

        t_put_representatives_list = LocalFilesystemToGCSOperator(
            task_id="t_put_representatives_list",
            src=path_list_representatives,
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

        (
            t_parse_representatives_list
            >> t_put_representatives_list
            >> t_load_source_m_representatives
            >> t_ctas_dwh_m_representatives
        )

    sql_ctas_mart_meeting_list = read_sql_file(
        "/workspaces/PoliQuant/sql/ctas_mart_meeting_list.sql"
    )
    t_ctas_mart_meeting_list = BigQueryInsertJobOperator(
        task_id="t_ctas_mart_meeting_list",
        configuration={
            "query": {
                "query": sql_ctas_mart_meeting_list,
                "useLegacySql": False,
            }
        },
        gcp_conn_id="google_cloud_default",
        location="US",
    )

    sql_ctas_mart_m_councilors_aggregated = read_sql_file(
        "/workspaces/PoliQuant/sql/ctas_mart_m_councilors_aggregated.sql"
    )
    t_ctas_mart_m_councilors_aggregated = BigQueryInsertJobOperator(
        task_id="t_ctas_mart_m_councilors_aggregated",
        configuration={
            "query": {
                "query": sql_ctas_mart_m_councilors_aggregated,
                "useLegacySql": False,
            }
        },
        gcp_conn_id="google_cloud_default",
        location="US",
    )

    sql_ctas_mart_m_representatives_aggregated = read_sql_file(
        "/workspaces/PoliQuant/sql/ctas_mart_m_representatives_aggregated.sql"
    )
    t_ctas_mart_m_representatives_aggregated = BigQueryInsertJobOperator(
        task_id="t_ctas_mart_m_representatives_aggregated",
        configuration={
            "query": {
                "query": sql_ctas_mart_m_representatives_aggregated,
                "useLegacySql": False,
            }
        },
        gcp_conn_id="google_cloud_default",
        location="US",
    )

    end = EmptyOperator(
        task_id="end",
    )

    # fmt: off
    start >> [g_meeting_list, g_councilors, g_representatives] >> t_ctas_mart_meeting_list
    [g_meeting_list, g_councilors] >> t_ctas_mart_m_councilors_aggregated
    [g_meeting_list, g_representatives] >> t_ctas_mart_m_representatives_aggregated
    [t_ctas_mart_meeting_list, t_ctas_mart_m_councilors_aggregated, t_ctas_mart_m_representatives_aggregated] >> end
