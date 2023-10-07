from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    url: str = Field("https://", env=".env", alias='URL')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


conf = Settings()
