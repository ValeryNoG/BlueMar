from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor

with DAG(dag_id='airbyte_trigger_job_example_async',
         default_args={'owner': 'airflow'},
         schedule_interval='@daily',
         start_date=days_ago(1)
    ) as dag:

    async_money_to_json = AirbyteTriggerSyncOperator(
        task_id='airbyte_async_money_json_example',
        airbyte_conn_id='airbyte_conn',  # Ensure this has the correct URL
        connection_id='92477fbf-5151-4f35-a51f-ea3514a181d0',
        asynchronous=True,
    )

    airbyte_sensor = AirbyteJobSensor(
        task_id='airbyte_sensor_money_json_example',
        airbyte_conn_id='airbyte_conn',  # Ensure this has the correct URL
        airbyte_job_id=async_money_to_json.output
    )

    async_money_to_json >> airbyte_sensor
