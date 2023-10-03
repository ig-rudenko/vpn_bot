from aiogram import types
from aiogram.exceptions import TelegramBadRequest

from .utils import generate_qr_code
from ..handlers.deleter import get_delete_back_button
from ..text import VPN_CONNECTION_ATTENTION


async def answer_connection_config(callback: types.CallbackQuery, connection_str: str):
    """
    Функция генерирует QR-код из заданной строки подключения, удаляет исходное сообщение и
    отправляет новое сообщение с QR-кодом в качестве фотографии и строкой подключения в качестве подписи.

    :param callback: Параметр callback имеет тип types.CallbackQuery и представляет объект запроса обратного вызова,
     который активировал функцию
    :param connection_str: Параметр Connection_str представляет собой строку,
     которая представляет конфигурацию соединения. Она используется для генерации QR-кода
     и отображения его в виде фотографии в сообщении Telegram.
    """
    qr_code: bytes = generate_qr_code(connection_str)
    image = types.BufferedInputFile(qr_code, filename="connection.jpg")
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
    await callback.message.answer_photo(
        photo=image,
        caption=f"Подключение было создано\n\n<code>{connection_str}</code>\n\n{VPN_CONNECTION_ATTENTION}",
        reply_markup=get_delete_back_button(),
        parse_mode="HTML",
    )
