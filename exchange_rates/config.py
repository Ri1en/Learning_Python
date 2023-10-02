from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    currency_xml_url: str = Field(
        "XML", env="exchange_rates.env", alias='CURRENCY_XML_URL'
    )
    model_config = SettingsConfigDict(env_file='exchange_rates.env', env_file_encoding='utf-8')


settings = Settings()
