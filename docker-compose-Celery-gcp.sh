docker build --rm --build-arg AIRFLOW_DEPS="gcp" -t hcl/docker-airflow:1.0 .
sed 's/image_tag/hcl\/docker-airflow:1.0/g' docker-compose-CeleryExecutor-template.yml > docker-compose-CeleryExecutor-gcp.yml
docker-compose -f docker-compose-CeleryExecutor-gcp.yml up -d