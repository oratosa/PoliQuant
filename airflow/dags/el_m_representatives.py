from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from datetime import datetime

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

with DAG(
    "extract_n_load_m_representatives_to_BigQuery",
    default_args=default_args,
    schedule_interval="0 0 3 * *",
    catchup=False,
) as dag:

    def generate_m_representatives():
        print("Generated a representatives list.")

    def put_m_representatives():
        print("Put the files of the generated representatives list on a GCS bucket.")

    def load_representatives_files_to_source_table():
        print(
            "Loaded the files of the representatives list into a source table in BigQuery."
        )

    def transform_the_source_table_of_representatives():
        print(
            "Transformed the rows in the source table of representatives and inserted them into the table in the dwh layer."
        )

    def create_the_dwh_table_of_sessions():
        print("Created the dwh table of sessions from dwh.meeting_list using CTAS.")

    def transform_the_dwh_table_of_representatives():
        print(
            "Transformed the rows in the dwh table of representatives and inserted them into the table in the mart layer."
        )

    t_generate_m_representatives = PythonOperator(
        task_id="generate_representatives_list_task",
        python_callable=generate_m_representatives,
    )

    t_put_m_representatives = PythonOperator(
        task_id="put_representatives_list_task",
        python_callable=put_m_representatives,
    )

    t_load_representatives_lists = PythonOperator(
        task_id="load_representatives_list_task",
        python_callable=load_representatives_files_to_source_table,
    )

    t_transform_source_representatives = PythonOperator(
        task_id="transform_source_representatives_list_task",
        python_callable=transform_the_source_table_of_representatives,
    )

    t_external_task_sensor = ExternalTaskSensor(
        task_id="waiting_for_dwh_meeting_list_being_created",
        external_dag_id="extract_n_load_meeting_list_to_BigQuery",
        external_task_id="transform_source_meeting_list_task",
        timeout=600,
        allowed_states=["success"],
        failed_states=["failed", "skipped"],
        mode="reschedule",
    )

    t_create_dwh_sessions = PythonOperator(
        task_id="create_dwh_session_table_task",
        python_callable=create_the_dwh_table_of_sessions,
    )

    t_transform_dwh_representatives = PythonOperator(
        task_id="transform_dwh_representatives_list_task",
        python_callable=transform_the_dwh_table_of_representatives,
    )

    (
        t_generate_m_representatives
        >> t_put_m_representatives
        >> t_load_representatives_lists
        >> t_transform_source_representatives
        >> t_external_task_sensor
        >> t_create_dwh_sessions
        >> t_transform_dwh_representatives
    )
