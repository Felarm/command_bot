import asyncio

from aiogram import Bot, Dispatcher

from clients.base import ApiClients
from config import settings
from handlers.auth import auth_router


services_clients = ApiClients()

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(
        auth_router
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
