from Get_weather.get_weather import get_weather_from_api
from Get_weather.postgres_db import PostgresDb
from Get_weather.db_config import PostgresSettings
from Get_weather.get_weather import MyModel


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
        self.data = None

    def get_weather_from_db(self) -> tuple:
        with PostgresDb(self.db_settings) as cursor:
            cursor.execute(f"""
            SELECT * FROM {self.db_settings.pg_table_name}
            WHERE city = %s
            """, (self.city,))
            rows: tuple = cursor.fetchall()
            cursor.close()
            return rows

    def save_weather_data(self, data_object: MyModel) -> None:
        with PostgresDb(self.db_settings) as cursor:
            insert_query: str = (f"""
            INSERT INTO {self.db_settings.pg_table_name} (city, temp, temp_max, temp_min, weather, weather_description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (
                data_object.city,
                data_object.temp,
                data_object.temp_max,
                data_object.temp_min,
                data_object.weather[0]['main'],
                data_object.weather[0]['description']
            ))
            cursor.close()

    def fetch_weather(self) -> tuple | MyModel | None:
        if self.get_weather_from_db():
            return self.get_weather_from_db()
        else:
            self.data = self.get_weather_from_api_service(self.city)
            self.save_weather_data(self.data)
            return self.data

    def __call__(self, *args, **kwargs) -> None:
        self.city: str = args[0]
        print(self.fetch_weather())


if __name__ == '__main__':
    settings = PostgresSettings()
    database = PostgresDb(settings)
    some_api_service = get_weather_from_api
    weather_object = Weather(database, settings, some_api_service)
    weather_object("Birmingham")
