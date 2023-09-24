from get_weather import get_weather_from_api
from postgres_db import PostgresDb
from db_config import PostgresSettings
from get_weather import MyModel


class Weather:
    def __init__(
            self,
            data_base_object: PostgresDb,
            settings_object: PostgresSettings,
            api_service: get_weather_from_api
    ):
        self.db = data_base_object
        self.db_settings = settings_object
        self.get_weather_from_api_service = api_service

    def get_weather_from_db(self) -> tuple:
        with PostgresDb(self.db_settings) as cursor:
            cursor.execute("""
            SELECT * FROM weather_table
            WHERE city = %s
            """, (self.city,))
            rows: tuple = cursor.fetchall()
            cursor.close()
            return rows[:-1]

    def fetch_weather(self) -> tuple | MyModel | None:
        if self.get_weather_from_db():
            return self.get_weather_from_db()
        else:
            return self.get_weather_from_api_service(self.city)

    def __call__(self, *args, **kwargs) -> None:
        self.city: str = args[0]
        print(self.fetch_weather())


if __name__ == '__main__':
    settings = PostgresSettings()
    database = PostgresDb(settings)
    some_api_service = get_weather_from_api
    weather_object = Weather(database, settings, some_api_service)
    weather_object("Ankara")


