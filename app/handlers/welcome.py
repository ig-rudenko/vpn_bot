from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..service.account import ProfileService
from ..models import User

router = Router()


async def get_welcome_keyboard(tg_id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if not await ProfileService.exist(tg_id):
        builder.row(
            types.InlineKeyboardButton(
                text="⏺ Войти",
                callback_data="login",
            ),
            types.InlineKeyboardButton(
                text="▶️Зарегистрироваться",
                callback_data="register",
            ),
        )
    builder.row(
        types.InlineKeyboardButton(
            text="🔗 Выбрать подключение",
            callback_data="tariff_selection",
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🌐 Проверить доступность сайта",
            callback_data="utils:url_check",
        )
    )
    return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await User.create_if_not_exist(tg_user=message.from_user)
    keyboard = await get_welcome_keyboard(message.from_user.id)
    await message.answer("Hello!", reply_markup=keyboard)
