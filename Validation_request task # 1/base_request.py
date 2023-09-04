from my_exeptions import MethodError


class BaseRequest:
    available_methods: list[str] = ["GET", "POST"]

    def __init__(self,  url: str, method: str, params: dict = None, body: str = None):
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
        if self.method not in self.available_methods:
            raise MethodError("The request method can only be GET or POST")

    def is_valid_body(self):
        if self.body and (self.method in "GET"):
            raise MethodError("The request method GET can't take attribute body")
