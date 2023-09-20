from aiogram import Router, types
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiohttp import ClientConnectorError, InvalidURL

from ..decorators.limiter import rate_limit
from ..service.utils import CheckURLAvailability
from ..states.utils import CheckURLState

router = Router()


@router.callback_query(F.data == "utils:url_check")
@rate_limit(60)
async def check_url_availability(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите интересующий вас URL адрес")
    await state.set_state(CheckURLState.url)
    await callback.answer()


@router.message(CheckURLState.url)
async def run_url_checker(message: types.Message, state: FSMContext):
    url = message.text
    status: int = 0
    try:
        status = await CheckURLAvailability(url).get_status_code()
    except InvalidURL:
        text = "❗️Неверный URL!"
    except ClientConnectorError:
        text = "❗️Не удалось получить доступ, если указанный вами адрес верный, значит доступ запрещен"
    else:
        if 100 <= status <= 401 or 404 < status < 500:
            text = "✅ Ресурс через VPN подключение доступен!"
        elif status == 403:
            text = "❌ Ресурс заблокирован для VPN подключения :("
        elif status == 404:
            text = "❔ Данная страница не существует"
        else:
            text = (
                "❎ Ресурс через VPN подключение доступен!\n"
                "Но произошла ошибка на стороне сервера"
            )
    if status:
        text += f"\nСтатус: {status}"
    await message.answer(text)
    await state.clear()
