from datetime import datetime
from functools import lru_cache
import re
import requests
from config import Settings
from pydantic import BaseModel, Field
from my_exeptions import ValidError


class MyModel(BaseModel):
    currency_quotes: dict = Field(alias='quotes')


def retry_decorator(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("Error", e)
            func(*args, **kwargs)
    return _wrapper


@retry_decorator
def get_currency_rate(char_code: str) -> tuple[str, float, datetime]:
    settings: dict = get_settings(rate_url=True)
    response = requests.get(settings['url'].format(api_key=settings['api_key'], char_code=char_code))
    data: dict = response.json()
    model_object = MyModel.model_construct(**data)
    currency_rate: float = model_object.currency_quotes[f"USD{char_code}"]
    currency_name: str = get_currency_name(char_code)
    return currency_name, currency_rate, datetime.now()


def get_currency_name(char_code: str) -> str:
    settings: dict = get_settings(name_url=True)
    response = requests.get(settings['url'].format(api_key=settings['api_key']))
    data: dict = response.json()
    currency_name: str = data[f"{char_code}"]
    return currency_name


@lru_cache
def get_settings(name_url=False, rate_url=False) -> dict | None:
    settings = Settings()
    if name_url:
        return {'api_key': settings.api_key, 'url': settings.get_currency_name_url}
    elif rate_url:
        return {'api_key': settings.api_key, 'url': settings.get_currency_rate_url}
    else:
        return None


def is_valid_code(char_code):
    if not re.fullmatch(r"^[A-Z]{3}$", char_code):
        raise ValidError("Invalid code")
