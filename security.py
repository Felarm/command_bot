from datetime import datetime, UTC

from jose import jwt, JWTError

from config import settings
from exceptions import TokenDecodeException


class JWTService:
    @staticmethod
    def get_token_exat(encoded_token: str) -> int:
        try:
            payload = jwt.decode(encoded_token, settings.SECRET_KEY, settings.ALGORITHM)
        except JWTError as e:
            raise TokenDecodeException("Wrong token data") from e
        return payload["exp"]
