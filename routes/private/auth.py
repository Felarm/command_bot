from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from clients.clients import ServicesClients
from exceptions import UsersClientException

auth_router = Router()


@auth_router.message(Command("start"))
async def cmd_start(message: Message, services_clients: ServicesClients):
    await message.answer("Sync in progress...")
    try:
        await services_clients.user_service_client.register_tg_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
        )
        await message.answer(f"Authed successful")
    except UsersClientException as err:
        logger.error(err)
        await message.answer(err.msg)
    except Exception as err:
        logger.error(err)
        await message.answer(f"Some thing went wrong, try again later")
