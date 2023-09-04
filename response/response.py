from my_exeptions import TimeOutError


class Response:
    def __init__(self, url: str, method: str, params: dict, status: int, timeout: int, status_text: str, content: str):
        self.url: str = url
        self.method: str = method
        self.params: dict = params
        self.status: int = status
        self.timeout: int = timeout
        self._time_out_check()
        self._status_text: str = status_text
        self._status_text_init()
        self.content: str = content

    @property
    def status_text(self) -> str:
        return self._status_text

    def _status_text_init(self) -> None:
        if self.status == 200 and self.method == "GET":
            self._status_text: str = "OK"
        if self.status == 201 and self.method == "POST":
            self._status_text: str = "CREATED"
        if self.status == 400:
            self._status_text: str = "BAD_REQUEST"
        if self.status == 404:
            self._status_text: str = "NOT_FOUND"
        if self.status == 401:
            self._status_text: str = "NOT_AUTH"

    def _time_out_check(self) -> None:
        if self.timeout > 5:
            self.status: int = 408
            raise TimeOutError("timeout > 5")


if __name__ == '__main__':
    a = Response("ffdsf", "POST", {'q': 1, 'e': 2}, 200, 4, 'NOT OK', "Nice content")
    print(a.status_text)
