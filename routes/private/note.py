from datetime import UTC

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger
from pydantic import ValidationError

from clients.clients import ServicesClients
from routes.states import NoteCreationStates
from schemas.datetime_validation import DatetimeValidator
from schemas.task_n_note_service_contracts import NoteCreate

note_router = Router()


@note_router.message(Command("new_note"))
async def new_note(message: Message, state: FSMContext):
    await state.set_state(NoteCreationStates.new)
    await message.answer("Please, enter Note name")


@note_router.message(NoteCreationStates.new)
async def new_note_name(message: Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await state.set_state(NoteCreationStates.name_added)
    await message.answer("Please, enter description")


@note_router.message(NoteCreationStates.name_added)
async def new_note_description(message: Message, state: FSMContext):
    await state.update_data({"description": message.text})
    await state.set_state(NoteCreationStates.description_added)
    await message.answer("Please enter remind datetime in YYYY-MM-DD HH:MM format")


@note_router.message(NoteCreationStates.description_added)
async def new_note_remind_at(message: Message, state: FSMContext):
    try:
        input_dt = DatetimeValidator.model_validate({"input_dt": message.text})
    except ValidationError as err:
        logger.error(err)
        await message.answer("Please enter datetime in format YYYY-MM-DD HH:MM. For example: '1984-04-20 02:28'")
        return
    await state.update_data({"remind_at": input_dt.input_dt.astimezone(UTC)})
    await state.set_state(NoteCreationStates.remind_datetime_added)
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Confirm", callback_data="confirm"))
    kb.add(InlineKeyboardButton(text="Cancel", callback_data="cancel"))
    confirm_data = await state.get_data()
    await message.answer(
        text=f"Here is your new note data:\n"
             f"Name: {confirm_data['name']}\n"
             f"Description: {confirm_data['description']}\n"
             f"Remind at: {message.text}\n\n"
             f"Do you confirm?",
        reply_markup=kb.as_markup(),
    )


@note_router.callback_query(NoteCreationStates.remind_datetime_added, F.data == "confirm")
async def new_note_confirm(cb: CallbackQuery, state: FSMContext, services_clients: ServicesClients):
    note_data = await state.get_data()
    note_create_data = NoteCreate.model_validate(note_data)
    access_token = await services_clients.user_service_client.get_access_token(cb.from_user.id, cb.from_user.username)
    if not access_token:
        await cb.message.answer("Something went wrong")
    resp_data = await services_clients.tasks_n_notes_service_client.create_note(access_token, note_create_data)
    await cb.message.answer(f"Your note has id: {resp_data.id}")
    await state.clear()


@note_router.callback_query(NoteCreationStates.remind_datetime_added, F.data == "cancel")
async def new_note_cancel(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("Ok, cancel is cancel")
    await state.clear()

