"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStorageObjectUpdatedSensor
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019, 9, 3),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG("open_air", default_args=default_args, schedule_interval='0 0 1 1 *')


t3 = BashOperator(
    task_id="templated",
    bash_command="echo 'Hello World'",
    params={"my_param": "Parameter I passed in"},
    dag=dag,
)
