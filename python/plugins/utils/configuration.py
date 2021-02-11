from datetime import timedelta

batch = {
    'owner': "airflow",
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
    'provide_context': True,
}