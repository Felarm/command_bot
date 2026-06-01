from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from clients.base import ApiClients

class ClientServicesMiddleware(BaseMiddleware):
    def __init__(self, clients: ApiClients):
        super().__init__()
        self.services_clients = clients

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["services_clients"] = self.services_clients
        return await handler(event, data)
