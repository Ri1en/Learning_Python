from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    api_key: str = Field("key", env="API_KEY")
    city_url: str = Field("https://api.openweathermap.org", env="OW_CITY_URL", alias='ow_city_url')
    coord_url: str = Field("https://api.openweathermap.org", env="OW_COORD_URL", alias='ow_coord_url')
    local_city_url: str = Field("https://api.openweathermap.org", env="OW_LOCAL_CITY_URL", alias='ow_local_city_url')

    model_config = SettingsConfigDict(env_file='get_weather.env', env_file_encoding='utf-8')


if __name__ == '__main__':
    settings = Settings()
    print(settings.api_key)
    print(settings.model_config)
    print(settings.local_city_url)
