import random

import asyncio
import aiohttp
import asyncpg

from db_config import PostgresSettings
from config import conf
from sinchronious_functions import Users
from sandwitch_decorators.decorators import time_it_async

settings = PostgresSettings()


def user_generator() -> Users:
    firstnames: list[str] = [
        'Александр', 'Михаил', 'Иван', 'Андрей', 'Дмитрий', 'Сергей', 'Артем', 'Николай', 'Максим', 'Егор'
    ]
    random_firstname = random.choice(firstnames)
    lastnames: list[str] = [
        'Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов', 'Михайлов', 'Новиков', 'Федоров'
    ]
    random_lastname: str = random.choice(lastnames)
    some_user = Users(random_firstname, random_lastname, random.randint(1, 100))
    return some_user


async def add_user(db_pool) -> None:
    user = user_generator()
    insert_query: str = (f"""
                   INSERT INTO async_table (firstname , lastname, age)
                   VALUES ($1, $2, $3)
                   """)
    await db_pool.execute(insert_query,
                          user.firstname,
                          user.lastname,
                          user.age
                          )


async def get_requests(session) -> list[dict]:
    async with session.get(conf.url) as res:
        data: list[dict] = await res.read()
        return data


@time_it_async
async def main_1():
    tasks: list[asyncio.Task] = []
    async with aiohttp.ClientSession() as session:
        for _ in range(5):
            task: asyncio.Task = asyncio.create_task(get_requests(session))
            tasks.append(task)
        res = await asyncio.gather(*tasks)


@time_it_async
async def main_2():
    tasks = []
    db_pool = await asyncpg.create_pool(database=settings.pg_db_name,
                                        user=settings.pg_user,
                                        password=settings.pg_password,
                                        port=settings.pg_port,
                                        host=settings.pg_host)
    for _ in range(10_000):
        task = asyncio.create_task(add_user(db_pool))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main_1())
    asyncio.run(main_2())
