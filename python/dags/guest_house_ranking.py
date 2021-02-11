from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from constants import CREATE_EMR_CLUSTER
from core.cluster import Cluster
from core.elastic_cache import ElastiCacheOperator
from core.spark import SparkOperator
from jobs.ranking import guest_house_ranking as job
from schema.ranking import TABLES
from utils.configuration import batch
from utils.dependency import sequential_dependency

with DAG(job['name'], start_date=job['start_date'], schedule_interval=job['schedule_time'].get_cron, default_args=batch) as dag:
    create_emr_cluster = PythonOperator(
        task_id=CREATE_EMR_CLUSTER,
        trigger_rule= "all_success",
        python_callable= Cluster().create(task_name=job["name"], num_nodes=job["num_nodes"], emr_version="emr-6.0.0"),
        op_kwargs={
            "name": job["name"],
            "num_nodes": job["num_nodes"],
        }
    )

    terminate_emr_cluster = PythonOperator(
        task_id=CREATE_EMR_CLUSTER,
        trigger_rule="all_done",
        python_callable=Cluster.terminate(),
        op_kwargs={
            "create_task_id" : CREATE_EMR_CLUSTER
        }
    )

    build_guest_house_ranking_tables = [
        PythonOperator(task_id=table["task_name"], trigger_rule="all_success", python_callable=SparkOperator().submit_spark_job, op_kwargs={"class_path": table["class_path"], "args": ["specify date here.. ex) '2019-10-30'"]}) for table in TABLES
    ]

    sequential_dependency(build_guest_house_ranking_tables)

    upload_guest_house_ranking_to_ec = ElastiCacheOperator.upload_to_ec(
        task_name= "upload_guest_house_ranking_delivery_to_ec",
        ttl=60 * 60 * 24 * 7,
        sleep_between_fetch=1,
        custom_query= f"""
            SELECT category, business_ids
            FROM guset_house.ranking_delivery_partitioned
        """)

    create_emr_cluster >> build_guest_house_ranking_tables >> upload_guest_house_ranking_to_ec >> terminate_emr_cluster
