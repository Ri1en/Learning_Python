from get_exchange_rates import get_currency_rate
from postgres_db import PostgresDb
from db_config import PostgresSettings


class ExchangeRates:
    def __init__(
            self,
            data_base_object: PostgresDb,
            settings_object: PostgresSettings,
            api_service: get_currency_rate
    ):
        self.db = data_base_object
        self.db_settings = settings_object
        self.get_exchange_rates_service = api_service
        self.data = None

    def get_currency_rates_from_db(self) -> tuple:
        with PostgresDb(self.db_settings) as cursor:
            cursor.execute(f"""
            SELECT * FROM {self.db_settings.pg_table_name}
            WHERE currency_code = %s
            """, (self.char_code,))
            rows: tuple = cursor.fetchall()
            cursor.close()
            return rows

    def save_exchange_rates_data(self, data_object: tuple) -> None:
        data = (self.char_code,) + data_object
        with PostgresDb(self.db_settings) as cursor:
            cursor.execute(f"""
            INSERT INTO {self.db_settings.pg_table_name} ({self.db_settings.pg_columns})
            VALUES (%s, %s, %s, %s)
            """, data)
            cursor.close()

    def fetch_weather(self) -> tuple:
        if self.get_currency_rates_from_db():
            return self.get_currency_rates_from_db()
        else:
            self.data = self.get_exchange_rates_service(self.char_code)
            self.save_exchange_rates_data(self.data)
            return self.data

    def __call__(self, *args, **kwargs) -> None:
        self.char_code: str = args[0]
        print(self.fetch_weather())


if __name__ == '__main__':
    settings = PostgresSettings()
    database = PostgresDb(settings)
    service = get_currency_rate
    exchange = ExchangeRates(database, settings, service)
    exchange('USD')
