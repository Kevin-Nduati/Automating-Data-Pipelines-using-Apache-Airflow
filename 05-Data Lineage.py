import datetime
import logging

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

import sql_statements as sql


def load_trip_data_to_redshift(*args, **kwargs):
    aws_hook = AwsBaseHook('aws_credentials')
    credentials = aws_hook.get_credentials()
    redshift_hook = PostgresHook('redshift')
    sql_stmt = sql.COPY_STATIONS_SQL.format(credentials.access_key, credentials.secret_key)
    redshift_hook.run(sql_stmt)


dag = DAG(
    'redshift_configure',
    start_date=datetime.datetime.now()
)

create_trips_table = PostgresOperator(
    task_id = 'create_table',
    postgres_conn_id = 'redshift',
    sql = sql.CREATE_STATIONS_TABLE_SQL,
    dag=dag
)

copy_trips_task = PythonOperator(
    task_id = 'copy_to_redshift',
    dag = dag,
    python_callable=create_trips_table
)

location_traffic_task = PostgresOperator(
    task_id = "calculate_location_traffic",
    dag= dag,
    postgres_conn_id = 'redshift',
    sql = sql.LOCATION_TRAFFIC_SQL
)

create_trips_table >> copy_trips_task
copy_trips_task >> location_traffic_task