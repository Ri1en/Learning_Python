import pytest


import Get_weather


SETTINGS = Get_weather.PostgresSettings()


@pytest.fixture(scope='session', autouse=True)
def create_moderate_table(database_connection):
    create_weather_query = """
        CREATE TABLE IF NOT EXISTS test_weather_table (
        weather_id SERIAL PRIMARY KEY,
        city VARCHAR(255),
        temp REAL,
        temp_max REAL,
        temp_min REAL,
        weather VARCHAR(255),
        weather_description VARCHAR(255)
        )
        """

    clear_weather_query = " DELETE FROM test_weather_table"

    database_connection.cursor.execute(create_weather_query)
    database_connection.connection.commit()
    yield
    database_connection.cursor.execute(clear_weather_query)
    database_connection.connection.commit()


@pytest.fixture()
def save_weather_in_test_function(database_connection):
    def create_weather(
            city: str, temp: float, temp_min: float, temp_max: float, weather: dict):
        field_set = {'city', 'temp', 'temp_min', 'temp_max', 'weather', 'weather_description'}
        data_for_test = {'name': city,
                         'temp': temp,
                         'temp_max': temp_max,
                         'temp_min': temp_min,
                         'weather':  [{'main': weather[0]['main'], 'description': weather[0]['description']}]
                         }
        weather_model = Get_weather.MyModel.model_construct(_fields_set=field_set, **data_for_test)
        return weather_model
    return create_weather


@pytest.fixture()
def read_weather_in_test_function(database_connection):
    def read_from_db():
        insert_query = """
            SELECT * FROM test_weather_table
            """
        database_connection.cursor.execute(insert_query)
        rows: tuple = database_connection.cursor.fetchall()
        return rows
    return read_from_db


@pytest.fixture(scope='session')
def database_connection():
    db_connection = Get_weather.PostgresDb(SETTINGS)
    return db_connection
