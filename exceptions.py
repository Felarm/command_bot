class BaseAppException(Exception):
    pass


class UsersClientException(BaseAppException):
    pass


class UnauthorizedException(UsersClientException):
    pass


class ExpiredAccessTokenException(UnauthorizedException):
    pass


class ExpiredRefreshTokenException(UnauthorizedException):
    pass
