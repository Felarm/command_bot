import asyncio

from aiogram import Bot, Dispatcher

from config import settings
from routes.private.auth import auth_router
from middlewares.api_clients import ClientServicesMiddleware
from routes.private.note import note_router


services_clients_middleware = ClientServicesMiddleware()


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(
        auth_router,
        note_router
    )
    dp.message.middleware(services_clients_middleware)
    dp.callback_query.middleware(services_clients_middleware)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
