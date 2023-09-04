import re
from base_request import BaseRequest
from my_exeptions import MethodError, ParamsError, UrlError


class Request(BaseRequest):
    available_methods: list[str] = ["GET", "POST", "PUT", "PATCH"]

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
        if self.method not in self.available_methods:
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


