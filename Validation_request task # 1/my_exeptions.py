class UrlError(Exception):
    def __init__(self, *args) -> None:
        self.message = args[0] if args else None

    def __str__(self) -> str:
        return f"[Error INFO]: {self.message}"


class MethodError(Exception):
    def __init__(self, *args) -> None:
        self.message = args[0] if args else None

    def __str__(self) -> str:
        return f"[Error INFO]: {self.message}"


class ParamsError(Exception):
    def __init__(self, *args) -> None:
        self.message = args[0] if args else None

    def __str__(self) -> str:
        return f"[Error INFO]: {self.message}"
