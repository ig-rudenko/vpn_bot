from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..models import User
from ..text import WELCOME

router = Router()


async def get_welcome_keyboard(user: User) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🚦 Ваш статус",
            callback_data="profile",
        ),
        types.InlineKeyboardButton(
            text="🔑 Получить доступ",
            callback_data="tariff_selection",
        ),
    )

    if user.is_superuser:
        builder.row(
            types.InlineKeyboardButton(text="📊 XRAY", callback_data="xray"),
            types.InlineKeyboardButton(text="📋 Сервер", callback_data="server"),
        )
        builder.row(
            types.InlineKeyboardButton(
                text="⚙️ Клиенты", callback_data="clients_control"
            ),
            types.InlineKeyboardButton(
                text="⚙️ Неклиенты", callback_data="clients_lead"
            )
        )
    """
    builder.row(
        types.InlineKeyboardButton(
            text="🌐 Проверить доступность сайта",
            callback_data="utils:url_check",
        )
    )
    """
    builder.row(
        types.InlineKeyboardButton(
            text="ℹ️ Как подключаться",
            callback_data="install:info",
        ),
        types.InlineKeyboardButton(
            text='🎁 Поделиться',
            switch_inline_query='Я подключил себе PROXY\VPN 👍 и хочу порекомендовать его Вам 🤝'
        )
    )
    return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user = await User.get_or_create(tg_user=message.from_user)
    keyboard = await get_welcome_keyboard(user)
    await message.answer(WELCOME, reply_markup=keyboard, parse_mode="html")


@router.callback_query(F.data == "start")
async def callback_start(callback: types.CallbackQuery):
    user = await User.get_or_create(tg_user=callback.from_user)
    keyboard = await get_welcome_keyboard(user)
    await callback.message.edit_text(WELCOME, reply_markup=keyboard, parse_mode="html")
    await callback.answer()

