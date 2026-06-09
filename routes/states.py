from aiogram.fsm.state import StatesGroup, State


class NoteCreationStates(StatesGroup):
    new = State()
    name_added = State()
    description_added = State()
    remind_datetime_added = State()


class TaskCreationStates(StatesGroup):
    new = State()
    name_added = State()
    description_added = State()
    start_dt_added = State()
    end_dt_added = State()
