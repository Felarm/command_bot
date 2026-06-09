from datetime import UTC, datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger
from pydantic import ValidationError

from clients.clients import ServicesClients
from routes.states import TaskCreationStates
from schemas.datetime_validation import DatetimeValidator
from schemas.task_n_note_service_contracts import TaskCreate

task_router = Router()


@task_router.message(Command("new_task"))
async def new_task(message: Message, state: FSMContext):
    await state.set_state(TaskCreationStates.new)
    await message.answer("Please, enter task name")


@task_router.message(TaskCreationStates.new)
async def new_task_name(message: Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await state.set_state(TaskCreationStates.name_added)
    await message.answer("Please, enter task description")


@task_router.message(TaskCreationStates.name_added)
async def new_task_description(message: Message, state: FSMContext):
    await state.update_data({"description": message.text})
    await state.set_state(TaskCreationStates.description_added)
    await message.answer("Please enter task start datetime in YYYY-MM-DD HH:MM format")


@task_router.message(TaskCreationStates.description_added)
async def new_task_start_dt(message: Message, state: FSMContext):
    try:
        input_dt = DatetimeValidator.model_validate({"input_dt": message.text})
    except ValidationError as err:
        logger.error(err)
        await message.answer("Please enter datetime in format YYYY-MM-DD HH:MM. For example: '1984-04-20 02:28'")
        return
    await state.update_data({"start_dt": input_dt.input_dt.astimezone(UTC)})
    await state.set_state(TaskCreationStates.start_dt_added)
    await message.answer("Please enter task end datetime in YYYY-MM-DD HH:MM format")


@task_router.message(TaskCreationStates.start_dt_added)
async def new_task_end_dt(message: Message, state: FSMContext):
    try:
        input_dt = DatetimeValidator.model_validate({"input_dt": message.text})
    except ValidationError as err:
        logger.error(err)
        await message.answer("Please enter datetime in format YYYY-MM-DD HH:MM. For example: '1984-04-20 02:28'")
        return
    start_dt: datetime = await state.get_value("start_dt")
    end_dt = input_dt.input_dt.astimezone(UTC)
    if end_dt <= start_dt:
        await message.answer("Task should end after it starts, not before. Please enter correct task end datetime")
        return
    await state.update_data({"end_dt": end_dt})
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Confirm", callback_data="confirm"))
    kb.add(InlineKeyboardButton(text="Cancel", callback_data="cancel"))
    confirm_data = await state.get_data()
    await message.answer(
        text=f"Here is your new note data:\n"
             f"Name: {confirm_data['name']}\n"
             f"Description: {confirm_data['description']}\n"
             f"Task starts at: {start_dt.isoformat(sep=" ")}\n"
             f"Task ends at: {end_dt.isoformat(sep=" ")}\n\n"
             f"Do you confirm?",
        reply_markup=kb.as_markup(),
    )
    await state.set_state(TaskCreationStates.end_dt_added)


@task_router.callback_query(TaskCreationStates.end_dt_added, F.data == "confirm")
async def new_task_confirm(cb: CallbackQuery, state: FSMContext, services_clients: ServicesClients):
    task_data = await state.get_data()
    task_create_data = TaskCreate.model_validate(task_data)
    access_token = await services_clients.user_service_client.get_access_token(cb.from_user.id, cb.from_user.username)
    if not access_token:
        await cb.message.answer("Something went wrong")
    resp_data = await services_clients.tasks_n_notes_service_client.create_task(access_token, task_create_data)
    await cb.message.answer(f"Your task has id: {resp_data.id}")
    await state.clear()


@task_router.callback_query(TaskCreationStates.end_dt_added, F.data == "cancel")
async def new_note_cancel(cb: CallbackQuery, state: FSMContext):
    await cb.message.answer("Ok, cancel is cancel")
    await state.clear()

