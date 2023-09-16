from functools import lru_cache
import requests
from pydantic import BaseModel, Field
from my_exeptions import ValidError
import config
import re
import json


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


def is_valid_coord(coord) -> None:
    if not (coord.get("lat") and coord.get("lon")):
        raise ValidError("Parameter coord is invalid. Coord format {'lat': float value, 'lon': float value}")


def is_valid_city(city) -> None:
    if not re.fullmatch(r"^[A-Za-zА-Яа-я\s-]+$", city):
        raise ValidError("City name is invalid")


if __name__ == '__main__':

    coords: dict = {"lat": 51.5085, "lon": -0.12574}
    response = get_weather_from_api(None, coords, "mr")
    # response = get_weather_from_api("Moscow")
    print(response.city)
    print(response.weather)
    print(response.local_name)
