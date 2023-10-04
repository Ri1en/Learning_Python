import time


def message_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Начало выполнения функции..,")
        res = func(*args, **kwargs)
        print(f"Функция закончила своё выполнение...")
        return res
    return wrapper


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        time_of_function_work = end_time - start_time
        print(f"Функция выполнялась: {time_of_function_work}")
        return res
    return wrapper


def cath_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except Exception as e:
            print(f"Ошибка:{e}")
    return wrapper
