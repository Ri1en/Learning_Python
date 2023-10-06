import random

import requests

from config import conf
from db_config import PostgresSettings
from postgres_db import PostgresDb
from sandwitch_decorators.decorators import time_it


settings = PostgresSettings()


class Users:
    def __init__(self, firstname, lastname, age):
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.age: str = age


@time_it
def add_users() -> None:
    with PostgresDb(settings) as cursor:
        count = 0
        while count != 10000:
            user = user_generator()
            insert_query = (f"""
            INSERT INTO {settings.pg_table_name} ({settings.pg_columns})
            VALUES (%s, %s, %s)
            """)
            cursor.execute(insert_query, (
                user.firstname,
                user.lastname,
                user.age
            ))
            count += 1
        else:
            cursor.close()


@time_it
def get_requests() -> list[dict]:
    count: int = 0
    res = None
    while count != 5:
        res = requests.get(conf.url)
        count += 1
    return res.json()


def user_generator() -> Users:
    firstnames: list[str] = ['Александр', 'Михаил', 'Иван', 'Андрей', 'Дмитрий', 'Сергей', 'Артем', 'Николай', 'Максим', 'Егор']
    random_firstname: str = random.choice(firstnames)
    lastnames: list[str] = [
        'Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов', 'Михайлов', 'Новиков', 'Федоров'
    ]
    random_lastname: str = random.choice(lastnames)
    some_user = Users(random_firstname, random_lastname, random.randint(1, 100))
    return some_user


if __name__ == '__main__':
    add_users()
    get_requests()
