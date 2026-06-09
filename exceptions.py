class BaseAppException(Exception):
    def __init__(self, msg: str, error_from: str = "Unknown"):
        self.msg = msg
        self.error_from = error_from
        super().__init__(self.msg)


class UsersClientException(BaseAppException):
    def __init__(self, msg: str):
        super().__init__(msg=msg, error_from="Users client")


class ExpiredTokenException(BaseAppException):
    def __init__(self, token_type: str, error_from: str):
        self.token_type = token_type
        super().__init__(msg="Expired token", error_from=error_from)


class TokenDecodeException(BaseAppException):
    def __init__(self, msg: str):
        super().__init__(msg, error_from="JWTDecode")


class TasksNNotesClientException(BaseAppException):
    def __init__(self, msg: str):
        super().__init__(msg=msg, error_from="Task n Notes client")
