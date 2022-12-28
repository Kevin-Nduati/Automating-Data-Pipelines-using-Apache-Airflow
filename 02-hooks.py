import datetime
import logging

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook


def list_keys():
    hook = AwsBaseHook(aws_conn_id = 'aws_credentials')
    bucket = Variable('s3_bucket')
    logging.info(f"Listing keys from {bucket}")
    keys = hook.list_keys(bucket)
    for key in keys:
        logging.info(f"- s3://{bucket}/{key}")


def hello_world():
    logging.info('Hello World')

def current_time():
    logging.info(f"Current time is {datetime.datetime.utcnow().isoformat()}")

def working_dir():
    logging.info("Working directory is {os.getcwd()}")

def complete():
    logging.info('Congrats, your multi-part pipeline is complete')

dag = DAG(
    description = "aws_creds",
    schedule='@hourly',
    start_date = datetime.datetime.now() - datetime.timedelta(days=1),
        dag_id = "multipart"

)

list_task = PythonOperator(
    task_id = "list_keys",
    python_callable=list_keys,
    dag=dag
)