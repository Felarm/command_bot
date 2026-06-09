from typing import Optional

import redis.asyncio as aioredis
from config import settings
from schemas.users_service_contracts import TokenModelResponse, TokenType
from security import JWTService

redis_client = aioredis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)


async def get_user_token(user_id: int, token_type: str) -> Optional[str]:
    token = await redis_client.get(f"user:{user_id}:{token_type}")
    if not token:
        return None
    return token


async def save_user_tokens(user_id: int, user_tokens: TokenModelResponse) -> None:
    async with redis_client.pipeline(transaction=True) as pipe:
        await pipe.set(
            name=f"user:{user_id}:{TokenType.ACCESS.value}",
            value=user_tokens.access_token,
            exat=JWTService.get_token_exat(user_tokens.access_token)
        )
        await pipe.set(
            name=f"user:{user_id}:{TokenType.REFRESH.value}",
            value=user_tokens.refresh_token,
            exat=JWTService.get_token_exat(user_tokens.refresh_token)
        )
        await pipe.execute()
