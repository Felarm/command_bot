from functools import wraps

from httpx import AsyncClient, RequestError, codes, HTTPStatusError, HTTPError

from config import settings
from exceptions import UsersClientException
from schemas.token import UserTokens, RefreshTokenRequest
from schemas.users_service import UserRegisterData


def handle_users_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPStatusError as err:
            res = err.response
            code = res.status_code
            if code == codes.UNPROCESSABLE_ENTITY:
                pass
        except (Exception, HTTPError) as err:
            raise UsersClientException from err
    return wrapper

class UserServiceClient:
    def __init__(self, client: AsyncClient):
        self.client = client

    @handle_users_errors
    async def register_tg_user(self, user_id: int, username: str) -> UserTokens:
        register_data = UserRegisterData(
            username=username,
            tg_id=user_id,
        )
        response = await self.client.post(
            url=settings.USERS_REGISTER_ENDPOINT,
            json=register_data.model_dump(),
        )
        response.raise_for_status()
        if response.status_code != codes.CREATED:
            raise UsersClientException("User service could not create user")
        return UserTokens.model_validate(response.json())

    @handle_users_errors
    async def refresh_tokens(self, refresh_token: str) -> UserTokens:
        request_data = RefreshTokenRequest(refresh_token=refresh_token)
        response = await self.client.post(
            url=settings.USERS_REFRESH_ENDPOINT,
            json=request_data.model_dump(),
        )
        response.raise_for_status()
        if response.status_code != codes.OK:
            raise UsersClientException("Refresh token error")  # todo expired? invalid?
        return UserTokens.model_validate(response.json())

    @handle_users_errors
    async def login_tg_user(self, user_id: int, username: str) -> UserTokens:
        pass
