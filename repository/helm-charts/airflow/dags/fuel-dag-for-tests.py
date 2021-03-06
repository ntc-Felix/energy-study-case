from asyncio import tasks
from airflow import DAG
from airflow.models.baseoperator import chain
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor

# [START default_args]
default_args = {
    'owner': 'marlon saura felix rozindo',
    'start_date': datetime(2022, 6, 4),
    'depends_on_past': False,
    'email': ['marlon.saura@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)}
# [END default_args]

# [START instantiate_dag]
with DAG(
    'govbr-fuel-data-extraction-for-tests',
    default_args=default_args,
    schedule_interval='@once',
    tags=['development', 's3', 'sensor', 'minio', 'spark', 'operator', 'k8s', 'TESTS']
) as dag:

    staging_diesel_spark_operator = SparkKubernetesOperator(
        task_id='staging_diesel_spark_operator',
        namespace='processing',
        application_file='load_to_staging_diesel.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

    monitor_spark_staging_diesel = SparkKubernetesSensor(
        task_id='monitor_spark_staging_diesel',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='staging_diesel_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")


    staging_oil_spark_operator = SparkKubernetesOperator(
        task_id='staging_oil_spark_operator',
        namespace='processing',
        application_file='load_to_staging_oil.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

    monitor_spark_staging_oil = SparkKubernetesSensor(
        task_id='monitor_spark_staging_oil',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='staging_oil_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

    bronze_diesel_spark_operator = SparkKubernetesOperator(
        task_id='bronze_diesel_spark_operator',
        namespace='processing',
        application_file='load_to_bronze_diesel.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)
    
    monitor_spark_bronze_diesel = SparkKubernetesSensor(
        task_id='monitor_spark_bronze_diesel',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='bronze_diesel_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

    bronze_oil_spark_operator = SparkKubernetesOperator(
        task_id='bronze_oil_spark_operator',
        namespace='processing',
        application_file='load_to_bronze_oil.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)
    
    monitor_spark_bronze_oil = SparkKubernetesSensor(
        task_id='monitor_spark_bronze_oil',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='bronze_oil_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

    silver_fuel_spark_operator = SparkKubernetesOperator(
        task_id='silver_fuel_spark_operator',
        namespace='processing',
        application_file='load_to_silver.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)
    
    monitor_spark_silver_fuel = SparkKubernetesSensor(
        task_id='monitor_spark_silver_fuel',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='silver_fuel_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

    gold_fuel_spark_operator = SparkKubernetesOperator(
        task_id='gold_fuel_spark_operator',
        namespace='processing',
        application_file='load_to_gold.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)
    
    monitor_spark_gold_fuel = SparkKubernetesSensor(
        task_id='monitor_spark_gold_fuel',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='gold_fuel_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

    chain(staging_diesel_spark_operator
        , monitor_spark_staging_diesel 
        , staging_oil_spark_operator 
        , monitor_spark_staging_oil
        , bronze_diesel_spark_operator
        , monitor_spark_bronze_diesel
        , bronze_oil_spark_operator
        , monitor_spark_bronze_oil
        , silver_fuel_spark_operator
        , monitor_spark_silver_fuel
        , gold_fuel_spark_operator
        , monitor_spark_gold_fuel)

