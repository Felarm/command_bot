from httpx import AsyncClient

from clients.users_service import UserServiceClient
from config import settings


class ApiClients:
    def __init__(self):
        self._users_client = AsyncClient(
            base_url=settings.USERS_SERVICE_URL,
            headers={"Authorization": f"Bearer {settings.USERS_SERVICE_TOKEN}"}
        )
        self.user_service_client = UserServiceClient(self._users_client)

    async def close_all(self):
        await self._users_client.aclose()
