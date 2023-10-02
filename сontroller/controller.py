import random
import string
import response_task_2


def get_random_url_params() -> dict:
    params: dict = {}
    for _ in range(0, random.randint(1, 5)):
        params[''.join(random.choice(string.ascii_lowercase))] = random.randint(1, 5)
    return params


def get_random_url() -> str:
    random_urls_list: list[str] = [

        "http://" + ''.join((random.choice(string.ascii_lowercase)) for _ in range(4)) + ".com" for _ in range(5)
    ]

    return random.choice(random_urls_list)


def get_random_status() -> int:
    available_status_list: list[int] = [200, 201, 400, 401, 404]
    random_status_list: list[int] = [random.randint(100, 200) for _ in range(5)]
    status_list: list[int] = available_status_list + random_status_list
    random.shuffle(status_list)
    return random.choice(status_list)


def get_random_method() -> str:
    available_method_list: list[str] = ["GET", "POST", "PUT", "PATCH"]

    return random.choice(available_method_list)


def get_random_params() -> dict:
    return {
            'method': get_random_method(),
            'status': get_random_status(),
            'request_time': random.randint(1, 10),
            'url': get_random_url(),
            'params': get_random_url_params()
            }


def retry(max_retries, generate_params_func):
    def retry_decorator(func):
        def _wrapper(*args, **kwargs):
            dict_of_parameters: dict = generate_params_func()
            available_status = [200, 201]
            for _ in range(max_retries):
                if args[4] not in available_status:
                    func(
                         dict_of_parameters["url"],
                         dict_of_parameters["params"],
                         dict_of_parameters["request_time"],
                         dict_of_parameters["method"],
                         dict_of_parameters["status"]
                         )
                else:
                    return func(*args, **kwargs)

        return _wrapper
    return retry_decorator


@retry(10, get_random_params)
def controller(url: str, params: dict, request_time: int, method: str, status: int) -> response_task_2.Response | None:
    return response_task_2.Response(url, method, params, status, random.randint(1, 10), "Status text",
                                    "Content")


if __name__ == '__main__':
    for i in range(10):
        dict_with_params: dict = get_random_params()
        try:
            response_object: response_task_2.Response | None = (
                controller(
                    dict_with_params["url"],
                    dict_with_params["params"],
                    dict_with_params["request_time"],
                    dict_with_params["method"],
                    dict_with_params["status"]
                ))

            print(response_object.status_text)
        except AttributeError:
            print("Wrong request")





