import os
from hmac import compare_digest

from aiogram import types
from aiogram import Router, F
from aiogram.filters import Command

from app.models import User
from app.handlers.welcome import get_welcome_keyboard

router = Router()


@router.message(Command("become"))
async def become_admin(message: types.Message):
    _, token = message.text.split()
    user = await User.get_or_create(message.from_user)

    if compare_digest(token, os.getenv("BECOME_TOKEN")):
        user.is_superuser = True
        await user.update(is_superuser=True)
        await message.answer(
            "Вы стали суперпользователем",
            reply_markup=await get_welcome_keyboard(user),
        )

    else:
        await message.answer(
            "Нет доступа",
            reply_markup=await get_welcome_keyboard(user),
        )
