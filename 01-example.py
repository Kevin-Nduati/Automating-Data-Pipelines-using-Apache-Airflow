import datetime
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator

def greet():
    logging.info('Hello World')

dag = DAG(
    description='Introduction to DAGs',
    start_date=datetime.datetime.now(),
    dag_id="003"
)

greet_task = PythonOperator(
    task_id = "print hello world",
    python_callable= greet,
    dag = dag
)