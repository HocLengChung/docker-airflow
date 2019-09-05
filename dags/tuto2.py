"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStoragePrefixSensor
from airflow.operators.mysql_operator import MySqlOperator
from datetime import datetime, timedelta
import sys, os


try:

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

    sense_gcs = GoogleCloudStoragePrefixSensor(
        task_id='sense_openair',
        bucket='dataflow-staging-europe-west1-984164108593',
        prefix='OpenAir',
        dag=dag)
    SQL = 'TRUNCATE `ProjectTracker`.`OpenAirN`;'

    do_mysql = MySqlOperator(task_id='mysql',
                             sql=SQL, mysql_conn_id='ppmo_mysql',
                             database='ProjectTracker',
                             dag=dag)


except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    raise Exception('exc_type: ' + str(exc_type) + 'fname, ' + str(fname) + 'exc_tb.tb_lineno' + str(exc_tb.tb_lineno))