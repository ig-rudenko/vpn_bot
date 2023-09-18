from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import User
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..service.account import Profile

router = Router()


async def get_keyboard(from_user: User) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if not await Profile.exist(from_user.id):
        builder.row(
            types.InlineKeyboardButton(
                text="Зарегистрироваться",
                callback_data="register",
            )
        )

    return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = await get_keyboard(message.from_user)
    await message.answer("Hello!", reply_markup=keyboard)
