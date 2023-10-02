from functools import lru_cache
import re


import json
import requests
from pydantic import BaseModel, Field


from Get_weather.my_exeptions import ValidError
from Get_weather.postgres_db import PostgresDb
from Get_weather.postgres_db import get_db_config
from Get_weather import config


class MyModel(BaseModel):
    language: str | None = Field(init_var=True, kw_only=True)
    local_name: str | None = Field(init_var=True, kw_only=True)
    city: str = Field(pattern=r'^[A-Za-zА-Яа-я\s-]+$', alias='name')
    local_names: dict | None
    coord: dict
    temp: float
    temp_min: float
    temp_max: float
    humidity: float
    weather: list[dict]

    def kelvin_to_celsius_validate(self) -> None:
        self.temp = float('{:.3f}'.format(self.temp - 273))
        self.temp_max = float('{:.3f}'.format(self.temp_max - 273))
        self.temp_min = float('{:.3f}'.format(self.temp_min - 273))


@lru_cache()
def get_settings():
    return config.Settings()


def retry_decorator(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("Error", e)
            func(*args, **kwargs)
    return _wrapper


@retry_decorator
def get_weather_from_api(
         city: str | None = None,
         coord: dict | None = None,
         lang: str | None = None,
         api_key=get_settings().api_key) -> MyModel | None:

    field_set: set = {'name', 'coord', 'temp', 'temp_min', 'temp_max', 'humidity', 'weather'}
    if city:
        is_valid_city(city)
        url = get_settings().city_url
        res = requests.get(url.format(city=city, api_key=api_key))
        data: dict = res.json()
        model_object = MyModel.model_construct(_fields_set=field_set, **data, **data['main'])
        model_object.kelvin_to_celsius_validate()
        with open('weather_data.json', 'w') as file:
            json.dump(model_object.model_dump(), file)
        return model_object

    if coord:
        is_valid_coord(coord)
        local_name: None = None
        if lang:
            data: dict = get_locale_name_data(coord, api_key) | get_weather_coord_data(coord, api_key)
            model_object = MyModel.model_construct(
                _fields_set={'local_names'}, **data, language=lang
            )
            local_name = model_object.local_names[f'{lang}']
        else:
            data: dict = get_weather_coord_data(coord, api_key)

        model_object = MyModel.model_construct(_fields_set=field_set, **data, **data['main'])
        model_object.local_name = local_name
        model_object.kelvin_to_celsius_validate()
        with open('weather_data.json', 'w') as file:
            json.dump(model_object.model_dump(exclude={'local_names'}), file)
        return model_object
    return None


def get_locale_name_data(coord, api_key) -> dict:
    url = get_settings().local_city_url
    res = requests.get(url.format(coord_lat=coord['lat'], coord_lon=coord['lon'], api_key=api_key))
    data: list[dict] = res.json()
    return data[0]


def get_weather_coord_data(coord, api_key) -> dict:
    url = get_settings().coord_url
    res = requests.get(url.format(coord_lat=coord['lat'], coord_lon=coord['lon'], api_key=api_key))
    data: dict = res.json()
    return data


def save_weather_data(data_object: MyModel) -> None:
    config_object = get_db_config()
    with PostgresDb(config_object) as cursor:
        insert_query: str = ("""
        INSERT INTO weather_table (city, temp, temp_max, temp_min, weather, weather_description)
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


def get_weather_from_db(city: str) -> tuple:
    config_object = get_db_config()
    with PostgresDb(config_object) as cursor:
        cursor.execute("""
        SELECT * FROM weather_table
        WHERE city = %s
        """, (city,))
        rows: tuple = cursor.fetchall()
        cursor.close()
        return rows


def fetch_weather(city: str) -> tuple | MyModel | None:
    if get_weather_from_db(city):
        return get_weather_from_db(city)
    else:
        return get_weather_from_api(city)


def is_valid_coord(coord) -> None:
    if not (coord.get("lat") and coord.get("lon")):
        raise ValidError("Parameter coord is invalid. Coord format {'lat': float value, 'lon': float value}")


def is_valid_city(city) -> None:
    if not re.fullmatch(r"^[A-Za-zА-Яа-я\s-]+$", city):
        raise ValidError("City name is invalid")


if __name__ == '__main__':
    coords: dict = {"lat": 51.5085, "lon": -0.12574}