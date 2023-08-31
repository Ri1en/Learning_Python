class MethodError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"[Error INFO]: {self.message}"


class ParamsError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"[Error INFO]: {self.message}"


class BaseRequest:
    def __init__(self, url, method, params=None, body=None):
        self.url = url
        self.method = method
        self.params = params
        self.body = body
        self.is_valid_method()

    def is_valid_method(self):
        if self.method != ("GET" or "POST"):
            raise MethodError("The request method can only be GET or POST")
        if self.body and self.method == "GET":
            raise MethodError("The request method GET can't take attribute body")


class Request(BaseRequest):

    def __init__(self, url, method, params=None, body=None):
        super().__init__(url, method, params, body)
        self.is_valid_params()

    def is_valid_params(self):
        try:
            if len(list(self.params)) > 5:
                raise ParamsError("object of class Request can take 5 or less params")
        except TypeError:
            print("Attribute params only dict")


if __name__ == '__main__':
    request = Request("http://url.com", "GET", {'q': 1, 'd': 2})