from time import time

import asyncio
from asyncio import Semaphore


async def serv_customer(free_cashiers: Semaphore, customer: int) -> None:
    async with free_cashiers:
        await asyncio.sleep(customer)


async def serv_customers(cashiers_number: int, customers: list[int]) -> int:
    free_cashiers = Semaphore(value=cashiers_number)
    customers_to_serv = []
    for customer in customers:
        task = asyncio.create_task(serv_customer(free_cashiers, customer))
        customers_to_serv.append(task)
    start_time = time()
    await asyncio.gather(*customers_to_serv)
    end_time = time()
    return int(end_time - start_time)


if __name__ == '__main__':
    print(asyncio.run(serv_customers(4, [1, 2, 3, 4, 10])))
