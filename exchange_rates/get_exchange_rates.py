from datetime import datetime
import re
from re import Match

from bs4 import BeautifulSoup
import requests

from config import settings
from my_exeptions import ValidError


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
    is_valid_code(char_code)
    return parse_and_prepare_data(char_code, settings.currency_xml_url)


def parse_and_prepare_data(char_code: str, url: str) -> tuple:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'xml')
    currency_body = soup.find(string=f"{char_code}")
    currency_data = currency_body.find_parents("Valute")
    currency_name: Match = re.search(r"(?<=Name>).+?(?=</Name)", str(currency_data[0]))
    currency_rate: Match = re.search(r"(?<=Value>).+?(?=</Value)", str(currency_data[0]))
    exchange_rate_date: Match = re.search(r'(?<=Date=").+?(?=")', str(soup))
    float_currency_rate: float = float(currency_rate.group().replace(',', '.'))
    utf_8_currency_name: str = convert_cp1251_to_utf8(currency_name.group())
    return utf_8_currency_name, float_currency_rate, exchange_rate_date.group()


def convert_cp1251_to_utf8(text: str) -> str:
    unicode_text = text.encode('cp1251')
    utf8_text: str = unicode_text.decode('utf-8')
    return utf8_text


def is_valid_code(char_code) -> None:
    if not re.fullmatch(r"^[A-Z]{3}$", char_code):
        raise ValidError("Invalid code")
