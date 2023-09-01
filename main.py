import re


class UrlError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"[Error INFO]: {self.message}"


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
        self._url = url
        self.method = method
        self.is_valid_method()
        self.params = params
        self._body = body
        self.is_valid_body()

    @property
    def body(self):
        self.is_valid_body()
        return self._body

    @property
    def url(self):
        return self._url

    def is_valid_method(self):
        if self.method not in ["GET", "POST"]:
            raise MethodError("The request method can only be GET or POST")

    def is_valid_body(self):
        if self.body and (self.method in "GET"):
            raise MethodError("The request method GET can't take attribute body")


class Request(BaseRequest):

    def __init__(self, url, method, params=None, body=None):
        super().__init__(url, method, params, body)
        self.is_valid_method()
        self.is_valid_body()
        self.is_valid_params()
        self.is_valid_url()

    @property
    def body(self):
        self.is_valid_body()
        return self._body

    @property
    def url(self):
        self.is_valid_url()
        return self._url

    def is_valid_method(self):
        if self.method not in ["GET", "POST", "PUT", "PATCH"]:
            raise MethodError("The request method can only be GET,POST,PUT,PATCH")

    def is_valid_params(self):
        try:
            if self.params and len(list(self.params)) > 5:
                raise ParamsError("object of class Request can take 5 or less params")
        except TypeError:
            print("Attribute params only dict")

    def is_valid_url(self):
        valid_url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
        if not re.match(valid_url_pattern, self._url):
            raise UrlError("Wrong format url")

    def is_valid_body(self):
        if self._body and (self.method in "GET"):
            raise MethodError("The request method GET can't take attribute body")


if __name__ == '__main__':
    request = Request("1123", "GET", {'d': 1, 'b': 2})

