from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from clients.users_service import UserServiceClient
from database import redis_client, save_user_tokens

auth_router = Router()


@auth_router.message(Command("start"))
async def cmd_start(message: Message, command: CommandObject):
    if message.chat.type in ("group", "supergroup"):
        bot_user = await message.bot.get_me()
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(
            text="Auth",
            url=f"https://t.me{bot_user.username}?start=auth"
        ))
        await message.answer(
            f"Hello, {message.from_user.full_name}, you have to auth\n"
            f"Press button and pm bot",
            reply_markup=kb.as_markup()
        )
        return
    await message.answer("Sync in progress...")
    try:
        new_users_tokens = await UserServiceClient.register_tg_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
        )
        await save_user_tokens(message.from_user.id, new_users_tokens)
        await message.answer(f"Authed successful")
    except Exception as err:
        logger.exception(err)
        await message.answer(f"Some thing went wrong, try again later")
