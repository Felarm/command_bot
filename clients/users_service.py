from functools import wraps

from httpx import AsyncClient, HTTPStatusError, HTTPError, codes

from config import settings
from database import save_user_tokens, get_user_token
from exceptions import UsersClientException, ExpiredTokenException
from schemas.users_service_contracts import UserFromTg, TokenModelResponse, RefreshTokenRequest, TokenExceptionContent, \
    ErrorType, TokenType


def handle_users_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPStatusError as err:
            res_code = err.response.status_code
            res_data = err.response.json()
            if res_code == codes.UNAUTHORIZED:
                err_data = TokenExceptionContent.model_validate(res_data)
                if err_data.error_type == ErrorType.EXPIRED_TOKEN:
                    raise ExpiredTokenException(err_data.token_type.value, "Users service")
                raise UsersClientException(f"{err_data.detail}: {err_data.error_type}, token type: {err_data.token_type}")
            else:
                raise UsersClientException(res_data["detail"])
        except (HTTPError, Exception) as err:
            raise UsersClientException(err)
    return wrapper


class UserServiceClient:
    def __init__(self, client: AsyncClient):
        self.client = client

    @handle_users_errors
    async def register_tg_user(self, user_id: int, username: str) -> TokenModelResponse:
        register_data = UserFromTg(
            username=username,
            tg_id=user_id,
        )
        response = await self.client.post(
            url=settings.USERS_REGISTER_ENDPOINT,
            json=register_data.model_dump(),
        )
        response.raise_for_status()
        new_users_tokens = TokenModelResponse.model_validate(response.json())
        await save_user_tokens(user_id, new_users_tokens)
        return new_users_tokens

    @handle_users_errors
    async def refresh_tokens(self, user_id: int, refresh_token: str) -> TokenModelResponse:
        refresh_data = RefreshTokenRequest(refresh_token=refresh_token)
        response = await self.client.post(
            url=settings.USERS_REFRESH_ENDPOINT,
            json=refresh_data.model_dump(),
        )
        response.raise_for_status()
        new_users_tokens = TokenModelResponse.model_validate(response.json())
        await save_user_tokens(user_id, new_users_tokens)
        return new_users_tokens

    @handle_users_errors
    async def login_tg_user(self, user_id: int, username: str) -> TokenModelResponse:
        login_data = UserFromTg(
            username=username,
            tg_id=user_id,
        )
        response = await self.client.post(
            url=settings.USERS_LOGIN_ENDPOINT,
            json=login_data.model_dump(),
        )
        response.raise_for_status()
        new_users_tokens = TokenModelResponse.model_validate(response.json())
        await save_user_tokens(user_id, new_users_tokens)
        return new_users_tokens

    async def get_access_token(self, user_id: int, username: str = None) -> str | None:
        access_token = await get_user_token(user_id, TokenType.ACCESS.value)
        if access_token:
            return access_token
        refresh_token = await get_user_token(user_id, TokenType.REFRESH.value)
        if refresh_token:
            new_tokens = await self.refresh_tokens(user_id, refresh_token)
            return new_tokens.access_token
        if not username:
            raise UsersClientException("Username should be provided")
        new_tokens = await self.login_tg_user(user_id, username)
        return new_tokens.access_token
