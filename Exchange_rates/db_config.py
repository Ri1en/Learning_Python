from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class PostgresSettings(BaseSettings):

    model_config = SettingsConfigDict(env_file='db.env', env_file_encoding='utf-8')

    pg_columns_initialize: str = Field('rows', env='db.env', alias='PG_DB_COLUMNS_INITIALIZE')
    pg_columns: str = Field('rows', env='db.env', alias='PG_DB_COLUMNS')
    pg_table_name: str = Field('table_name', env='db.env', alias='PG_DB_TABLE_NAME')
    pg_host: str = Field('hostname', env='db.env', alias='PG_HOST')
    pg_user: str = Field('user', env='db.env', alias='PG_USER')
    pg_name: str = Field('db_name', env='db.env', alias='PG_DB_NAME')
    pg_password: str = Field('password', env='db.env', alias='PG_PASSWORD')
    pg_port: str = Field(5432, env='db.env', alias='PG_PORT')
