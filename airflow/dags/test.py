from datetime import datetime, timedelta

from airflow.models.dag import DAG

from airflow.operators.bash import BashOperator

default_args = {
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function, # or list of functions
    # 'on_success_callback': some_other_function, # or list of functions
    # 'on_retry_callback': another_function, # or list of functions
    # 'sla_miss_callback': yet_another_function, # or list of functions
    # 'on_skipped_callback': another_function, #or list of functions
    # 'trigger_rule': 'all_success'
}

with DAG(
    dag_id="test",
    default_args=default_args,
    description="A simple test DAG",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 5, 30),
    tags=["example"],
) as dag:

    t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

    t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)

    t3 = BashOperator(task_id="print_hello", bash_command='echo "hello world"', dag=dag)

    t1 >> t2 >> t3

