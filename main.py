class BaseRequest:
    def __init__(self, url, method, params=None, body=None):
        self.url = url
        try:
            self.method = method
            if self.method != ("GET" or "POST"):
                raise Exception
        except Exception as _ex:
            self.method = None
            print("Unknown method")
        self.params = params
        self.body = body

    def get_url(self):
        return self.url

    def get_method(self):
        return self.method

    def get_params(self):
        return self.params

    def get_body(self):
        return self.body


if __name__ == '__main__':
    request = BaseRequest("http://url.com", "GET", {'q': 1, 'd': 2})
