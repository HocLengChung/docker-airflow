gcsfuse -o nonempty -o allow_other airflow_vangogh-231409 dags
docker build --rm --build-arg AIRFLOW_DEPS="gcp" -t hcl/docker-airflow:1.0 .
sed 's/image_tag/hcl\/docker-airflow:1.0/g' docker-compose-CeleryExecutor-template.yml > docker-compose-CeleryExecutor-gcp.yml
docker-compose -f docker-compose-CeleryExecutor-gcp.yml up -d
docker exec -it docker-airflow_webserver_1 airflow connections -d --conn_id postgres_default
docker exec -it docker-airflow_webserver_1 airflow connections --add --conn_id ppmo_mysql --conn_uri mysql://ppmo-admin:DEVOTEAM@10.27.96.3:3306/ProjectTracker
docker exec -it docker-airflow_webserver_1 airflow connections --add --conn_id postgres_default --conn_uri postgresql+psycopg2://airflow:airflow@postgres:5432/airflow

