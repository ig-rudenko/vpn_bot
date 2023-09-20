from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..service.account import ProfileService
from ..models import User
from ..text import WELCOME

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
    else:
        builder.row(
            types.InlineKeyboardButton(
                text="Профиль",
                callback_data="profile",
            )
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
    await message.answer(WELCOME, reply_markup=keyboard)


@router.callback_query(F.data == "start")
async def cmd_start(callback: types.CallbackQuery):
    await User.create_if_not_exist(tg_user=callback.from_user)
    keyboard = await get_welcome_keyboard(callback.from_user.id)
    await callback.message.edit_text(WELCOME, reply_markup=keyboard)
    await callback.answer()
