"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStoragePrefixSensor
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators import DataFlowJavaXcomKeysOperator, GoogleCloudStorageListOperator, postgres_operator

from datetime import datetime, timedelta
import sys, os
# try:

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

delete_xcom_task = postgres_operator.PostgresOperator(
    task_id='delete-xcom-task',
    postgres_conn_id='postgres_default',
    sql="DELETE FROM xcom WHERE dag_id='{{ dag.dag_id }}'",
    dag=dag)

bucket = 'dataflow-staging-europe-west1-984164108593'
prefix = 'OpenAir'
sense_gcs = GoogleCloudStoragePrefixSensor(
    task_id='sense_openair_file_in_gcs',
    bucket=bucket,
    prefix=prefix,
    dag=dag)

SQL = 'TRUNCATE `ProjectTracker`.`OpenAirN`;'
truncate_mysql_table = MySqlOperator(
    task_id='truncate_openair_mysql_table',
    sql=SQL, mysql_conn_id='ppmo_mysql',
    database='ProjectTracker',
    dag=dag)

list_found_file = GoogleCloudStorageListOperator(
    task_id='list_found_file',
    bucket=bucket,
    prefix=prefix,
    dag=dag)
#
load_dataflow = DataFlowJavaXcomKeysOperator(
        task_id='execute_dataflow',
        jar='gs://dataflow_vangogh-231409/ppmo_dataflow-bundled-1.0.jar',
        options={
            'numWorkers': '1',
            'workerMachineType': 'n1-standard-2',
            'autoscalingAlgorithm': 'NONE',
            'usePublicIps': 'false',
        },
        gcp_conn_id='google_cloud_default',
        xcom_element_list=[
            {'xcom_key': 'MAX_UPD_TS',
             'task_id': 'list_found_file',
             'dataflow_par_name': 'inputFile'}],
        dag=dag)


delete_xcom_task >> list_found_file
sense_gcs >> truncate_mysql_table
sense_gcs >> list_found_file

# except Exception as e:
#     exc_type, exc_obj, exc_tb = sys.exc_info()
#     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#     raise Exception('exc_type: ' + str(exc_type) + 'fname, ' + str(fname) + 'exc_tb.tb_lineno' + str(exc_tb.tb_lineno))
