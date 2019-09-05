from airflow.plugins_manager import AirflowPlugin
from operators.dataflow_xcom_operator import DataFlowJavaXcomKeysOperator
from operators.gcs_list_operator import GoogleCloudStorageListOperator


class HclEtlPlugin(AirflowPlugin):
    name = "Custom"
    operators = [DataFlowJavaXcomKeysOperator, GoogleCloudStorageListOperator]
    # Leave in for explicitness
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []