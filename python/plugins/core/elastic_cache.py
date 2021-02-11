from airflow.operators.python_operator import PythonOperator
import json
import logging
from pyathena import connect
import redis
import time

# TODOs: Need to customize _parse_row for each serving table. --> Create {table'name}Operator and Inherit ElasticCacheOperator
class ElastiCacheOperator:
    def _parse_row(self, row) -> (str, dict):
        category = row[0]
        business_ids = row[1]

        key = f"guest_house:ranking:{category}"
        value_dict = {
            "shop_ids": json.loads(business_ids)
        }

        return key, value_dict

    def _get_redis_host(self) -> str:
        return "copy and paste your redis cluster's endpoint here"

    def _get_athena(self):
        return connect(
            s3_staging_dir="s3://..target table's loaction here..",
            region_name="region ex) ap-northeast-2",
            work_group="",
        ).cursor()

    def _get_redis(self):
        host = self._get_redis_host()

        return redis.Redis(host=host, port=6379, db=0)

    def _upload_to_ec(self, **kwargs) -> None:
        athena = self._get_athena()
        athena.execute(kwargs["custom_query"])

        r = self._get_redis()

        no_rows = 0
        no_failed = 0
        while True:
            rows = athena.fetchmany()
            for row in rows:
                try:
                    key, value_dict = self._parse_row(row)
                    value = json.dumps(value_dict)

                    if kwargs['ttl'] > 0:
                        r.setex(key, kwargs['ttl'], value)
                    else:
                        r.set(key, value)

                except json.decoder.JSONDecodeError as e:
                    no_failed += 1
                    logging.info(f"Failed to parse {row} with error {e}")

            no_rows += len(rows)
            logging.info(f"So far, {no_rows} rows have been successfully set")
            logging.info(f"So far, {no_failed} rows have been failed to set")

            time.sleep(kwargs['sleep_between_fetch'])

            if not rows:
                break

    @staticmethod
    def upload_to_ec(self, task_name: str, ttl: int, sleep_between_fetch: int, custom_query: str) -> PythonOperator:
        return PythonOperator(
            task_id=task_name,
            python_callable=self._upload_to_ec,
            op_kwargs={
                'ttl': ttl,
                'sleep_between_fetch': sleep_between_fetch,
                "custom_query" : custom_query
            },
        )
