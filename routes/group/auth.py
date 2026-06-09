from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger


group_router = Router()


@group_router.message(F.chat.type in ("group", "supergroup"), F.text == Command("start"))
async def cmd_start(message: Message):
    bot_user = await message.bot.get_me()
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Auth",
        url=f"https://t.me/{bot_user.username}?start=auth"
    ))
    await message.answer(
        f"Hello, {message.from_user.full_name}, you have to auth\n"
        f"Press button and pm bot",
        reply_markup=kb.as_markup()
    )
