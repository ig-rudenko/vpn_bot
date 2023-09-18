from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..service.utils import CheckURLAvailability
from ..states.utils import CheckURLState

router = Router()


@router.message(Command("checkurl"))
async def check_url_availability(message: types.Message, state: FSMContext):
    await message.answer("Введите интересующий вас URL адрес")
    await state.set_state(CheckURLState.url)


@router.message(CheckURLState.url)
async def run_url_checker(message: types.Message, state: FSMContext):
    url = message.text
    if CheckURLAvailability(url).available():
        await message.answer("Ресурс через VPN подключение доступен!")
    else:
        await message.answer("Ресурс заблокирован для VPN подключения :(")
    await state.clear()
