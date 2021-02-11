import logging
import time

import boto3
from typing import Tuple

class SparkOperator:

    def submit_spark_job(self, **kwargs) -> None:
        # ti: task instance
        cluster_id = kwargs['ti'].xcom_pull("create_emr_cluster")

        job_flow_args = [
            "spark-submit",
            "--class",
            kwargs["class_path"],
            "s3://../~.jar"
        ]

        job_flow_args.extend([str(arg) for arg in kwargs["args"]])

        response = boto3.client("emr").add_job_flow_steps(
            JobFlowId=cluster_id,
            Steps=[
                {
                    'Name': kwargs["class_path"],
                    'ActionOnFailure': "CONTINUE",
                    'HadoopJarStep': {
                        'Jar': "command-runner.jar",
                        'Args': job_flow_args,
                    },
                },
            ],
        )

        self._track_job_flow_steps(cluster_id, response["StepIds"])

    def _track_job_flow_steps(self, cluster_id: str, step_id: Tuple[str]) -> None:
        job_status = None

        while job_status != "FAILED" and job_status != "COMPLETED" and job_status != "CANCELLED":
            response = boto3.client("emr").list_steps(
                ClusterId=cluster_id,
                StepIds=step_id,
            )

            if not response:
                raise ValueError("Failed to track job progress!")

            # We assume that only one step is added
            job_status = response['Steps'][0]['Status']['State']
            logging.info(f"Current job status: {job_status}")

            time.sleep(10)

        if job_status == "FAILED" or job_status == "CANCELLED":
            raise ValueError("Job execution has been failed!")

        logging.info(f"Step {step_id} has been completed on {cluster_id}!")
