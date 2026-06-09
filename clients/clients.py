from httpx import AsyncClient

from clients.tasks_n_notes_service import TasksNNotesServiceClient
from clients.users_service import UserServiceClient
from config import settings


class ServicesClients:
    def __init__(self):
        self._users_client = AsyncClient(
            base_url=settings.USERS_SERVICE_URL,
            headers={"Authorization": f"Bearer {settings.USERS_SERVICE_TOKEN}"},
        )
        self.user_service_client = UserServiceClient(self._users_client)

        self._tasks_n_notes_client = AsyncClient(
            base_url=settings.TASKS_N_NOTES_SERVICE_URL,
            headers={"content-type": "application/json"}
        )
        self.tasks_n_notes_service_client = TasksNNotesServiceClient(self._tasks_n_notes_client)

    async def close_all(self):
        await self._users_client.aclose()
        await self._tasks_n_notes_client.aclose()
