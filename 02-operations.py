import datetime
import logging
import os

from airflow import DAG
from airflow.operators.python import PythonOperator


def hello_world():
    logging.info('Hello World')

def current_time():
    logging.info(f"Current time is {datetime.datetime.utcnow().isoformat()}")

def working_dir():
    logging.info("Working directory is {os.getcwd()}")

def complete():
    logging.info('Congrats, your multi-part pipeline is complete')

dag = DAG(
    description = "multipart",
    schedule_interval='@hourly',
    start_date = datetime.datetime.now() - datetime.timedelta(days=1)
)

hello_world_task = PythonOperator(
    task_id = 'hello_world',
    python_callable = hello_world,
    dag=dag
)

current_time_task = PythonOperator(
    task_id = 'current_time',
    python_callable = current_time,
    dag=dag
)

working_dir_task = PythonOperator(
    task_id = 'working_directory',
    python_callable = working_dir,
    dag=dag
)

complete_task = PythonOperator(
    task_id = 'complete',
    python_callable = complete,
    dag=dag
)

hello_world_task >> current_time_task
hello_world_task >> working_dir_task
current_time_task >> complete_task
working_dir_task >> complete_task