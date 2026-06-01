from typing import Optional

import redis.asyncio as aioredis
from config import settings
from schemas.token import UserTokens

redis_client = aioredis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)


async def get_user_tokens(user_id: int) -> Optional[UserTokens]:
    raw_tokens = redis_client.get(f"user:{user_id}:tokens")
    if not raw_tokens:
        return None
    return UserTokens.model_validate(raw_tokens)


async def save_user_tokens(user_id: int, user_tokens: UserTokens) -> None:
    redis_key = f"user:{user_id}:tokens"
    await redis_client.set(redis_key, user_tokens.model_dump_json())
