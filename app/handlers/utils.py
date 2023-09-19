from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiohttp import InvalidURL

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
    status: int = 0
    try:
        status = await CheckURLAvailability(url).get_status_code()
    except AttributeError as exc:
        text = "Неверный URL!"
    else:
        if 100 <= status <= 401 or 404 < status < 500:
            text = "Ресурс через VPN подключение доступен!"
        elif status == 403:
            text = "Ресурс заблокирован для VPN подключения :("
        elif status == 404:
            text = "Данная страница не существует"
        else:
            text = (
                "Ресурс через VPN подключение доступен!\n"
                "Но произошла ошибка на стороне сервера"
            )
    if status:
        text += f"\nСтатус: {status}"
    await message.answer(text)
    await state.clear()
