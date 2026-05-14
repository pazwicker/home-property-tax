import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

from .config import BQ_PROJECT, BQ_DATASET, BQ_LOCATION, YEAR_COLUMNS


def get_client() -> bigquery.Client:
    return bigquery.Client(project=BQ_PROJECT)


def ensure_dataset_exists(client: bigquery.Client) -> None:
    dataset_ref = bigquery.DatasetReference(BQ_PROJECT, BQ_DATASET)
    try:
        client.get_dataset(dataset_ref)
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = BQ_LOCATION
        client.create_dataset(dataset)
        print(f"Created dataset {BQ_PROJECT}.{BQ_DATASET}")


def delete_year(client: bigquery.Client, table_name: str, year: int) -> None:
    """Remove all rows for a given year so re-loading is idempotent."""
    year_col = YEAR_COLUMNS[table_name]
    full_table = f"`{BQ_PROJECT}.{BQ_DATASET}.{table_name}`"
    dml = f"DELETE FROM {full_table} WHERE CAST({year_col} AS STRING) = '{year}'"
    job = client.query(dml)
    job.result()


def table_exists(client: bigquery.Client, table_name: str) -> bool:
    table_ref = f"{BQ_PROJECT}.{BQ_DATASET}.{table_name}"
    try:
        client.get_table(table_ref)
        return True
    except NotFound:
        return False


def load_dataframe(client: bigquery.Client, df: pd.DataFrame, table_name: str) -> int:
    """Append a DataFrame to a BigQuery table. Returns number of rows written."""
    table_ref = f"{BQ_PROJECT}.{BQ_DATASET}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
        autodetect=True,
    )
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()
    return len(df)
