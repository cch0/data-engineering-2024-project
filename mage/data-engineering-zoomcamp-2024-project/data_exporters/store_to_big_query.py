from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
    # construct table id from env variables
    gcp_project_id=os.environ.get('GCP_PROJECT')
    bigquery_dataset=os.environ.get('BIGQUERY_DATASET')
    bigquery_table=os.environ.get('BIGQUERY_TABLE')
    table_id = f'{gcp_project_id}.{bigquery_dataset}.{bigquery_table}'

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        table_id,
        if_exists='append',  # Specify resolution policy if table name already exists
    )
