from functools import wraps

from httpx import AsyncClient, HTTPStatusError, HTTPError

from config import settings
from exceptions import TasksNNotesClientException
from schemas.task_n_note_service_contracts import NoteCreate, NoteModelResponse, TaskCreate, TaskModelResponse


def handle_tasks_n_notes_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPStatusError as err:
            raise TasksNNotesClientException(f"{err.response.status_code}\n{err}")
        except (HTTPError, Exception) as err:
            raise TasksNNotesClientException(err)
    return wrapper


class TasksNNotesServiceClient:
    def __init__(self, client: AsyncClient):
        self.client = client

    def _add_auth_header(self, token: str):
        self.client.headers["Authorization"] = f"Bearer {token}"

    @handle_tasks_n_notes_errors
    async def create_note(self, access_token: str, new_note_data: NoteCreate) -> NoteModelResponse:
        self._add_auth_header(access_token)
        response = await self.client.post(
            url=settings.CREATE_NOTE_ENDPOINT,
            content=new_note_data.model_dump_json(),
        )
        response.raise_for_status()
        return NoteModelResponse.model_validate(response.json())

    @handle_tasks_n_notes_errors
    async def create_task(self, access_token: str, new_task_data: TaskCreate) -> TaskModelResponse:
        self._add_auth_header(access_token)
        response = await self.client.post(
            url=settings.CREATE_TASK_ENDPOINT,
            content=new_task_data.model_dump_json(),
        )
        response.raise_for_status()
        return TaskModelResponse.model_validate(response.json())
