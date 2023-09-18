from aiogram.fsm.state import StatesGroup, State


class CheckURLState(StatesGroup):
    url = State()
