from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    api_key: str = Field("key", env="exchange_rates.env", alias='API_KEY')
    get_currency_name_url: str = Field(
        "https://openexchangerates.org/api/currencies", env="exchange_rates.env", alias='CURRENCY_NAME_URL'
    )
    get_currency_rate_url: str = Field(
        "https://openexchangerates.org/api/currencies", env="exchange_rates.env", alias='CURRENCY_RATE_URL'
    )

    model_config = SettingsConfigDict(env_file='exchange_rates.env', env_file_encoding='utf-8')


if __name__ == '__main__':
    settings = Settings()
    print(settings.api_key)
    print(settings.model_config)
