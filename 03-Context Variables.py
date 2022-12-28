import datetime
import logging

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook

def log_details(*args, **kwargs):
    # log date stamp
    logging.info(f"My execution date is {kwargs['ds']}")
    # log execution_date
    logging.info(f"My execution date is {kwargs['execution_date']}")




dag = DAG(
    'context',
    schedule='@daily',
    start_date=datetime.datetime.now() - datetime.timedelta(days=2),
    dag
)

list_task = PythonOperator(
    task_id = 'log_details',
    python_callable=log_details,
    dag=dag,
    provide_context=True
)