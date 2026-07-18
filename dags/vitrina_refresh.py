"""
DAG обновления витрины

Источник -> pandas DataFrame -> агрегация -> запись в Iceberg через pyiceberg.
Идемпотентно: витрина перезаписывается целиком, поэтому повторный запуск не даёт дублей.
"""
from datetime import datetime

import pandas as pd
import pyarrow as pa
from airflow import DAG
from airflow.operators.python import PythonOperator
from pyiceberg.catalog import load_catalog
from pyiceberg.exceptions import (
    NamespaceAlreadyExistsError,
    NoSuchTableError,
)

SOURCE_CONN = dict(
    host="source-db", port=5432, dbname="postgres", user="postgres", password="postgres"
)

CATALOG_CONF = {
    "type": "rest",
    "uri": "http://iceberg-rest:8181",
    "warehouse": "s3://warehouse/",
    "s3.endpoint": "http://minio:9000",
    "s3.access-key-id": "admin",
    "s3.secret-access-key": "password",
    "s3.region": "us-east-1",
    "s3.path-style-access": "true",
}

TABLE_NAME = "default.vitrina_production_by_field"

#Вот тут перепишу, как появится источник
def extract_and_build_vitrina(**_):
    import psycopg2

    conn = psycopg2.connect(**SOURCE_CONN)
    df = pd.read_sql(
        "SELECT record_date, field_name, SUM(volume_bbl) AS total_volume_bbl "
        "FROM production_daily GROUP BY record_date, field_name",
        conn,
    )
    conn.close()
    df["updated_at"] = datetime.utcnow()
    df.to_parquet("/tmp/vitrina.parquet")


def write_to_iceberg(**_):
    df = pd.read_parquet("/tmp/vitrina.parquet")
    table_data = pa.Table.from_pandas(df)

    catalog = load_catalog("default", **CATALOG_CONF)

    try:
        catalog.create_namespace(("default",))
    except NamespaceAlreadyExistsError:
        pass

    try:
        table = catalog.load_table(TABLE_NAME)
    except NoSuchTableError:
        table = catalog.create_table(
            identifier=TABLE_NAME,
            schema=table_data.schema,
        )

    table.overwrite(table_data)


with DAG(
    dag_id="vitrina_refresh",
    schedule_interval="*/5 * * * *",
    start_date=datetime(2026, 7, 1),
    catchup=False,
    default_args={"retries": 2},
) as dag:
    extract_task = PythonOperator(
        task_id="extract_and_build_vitrina",
        python_callable=extract_and_build_vitrina,
    )
    load_task = PythonOperator(
        task_id="write_to_iceberg",
        python_callable=write_to_iceberg,
    )
    extract_task >> load_task
