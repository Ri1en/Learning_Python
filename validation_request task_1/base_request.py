from my_exeptions import MethodError


class BaseRequest:
    available_methods: list[str] = ["GET", "POST"]

    def __init__(self,  url: str, method: str, params: dict | None, body: str | None) -> None:
        self._url: str = url
        self.method: str = method
        self.is_valid_method()
        self.params: dict = params
        self._body: str = body
        self.is_valid_body()

    @property
    def body(self) -> str:
        self.is_valid_body()
        return self._body

    @property
    def url(self) -> str:
        return self._url

    def is_valid_method(self) -> None:
        if self.method not in self.available_methods:
            raise MethodError("The request method can only be GET or POST")

    def is_valid_body(self) -> None:
        if self.body and (self.method == "GET"):
            raise MethodError("The request method GET can't take attribute body")
