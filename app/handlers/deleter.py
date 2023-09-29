from aiogram import F, Router, types

from app.handlers.welcome import get_welcome_keyboard
from app.models import User
from app.text import WELCOME

router = Router()


def get_delete_back_button():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="🔙 Назад", callback_data="delete-config")]
        ]
    )


@router.callback_query(F.data == "delete-config")
async def delete_config_image_and_go_start(callback: types.CallbackQuery):
    user = await User.get_or_create(callback.from_user)
    await callback.message.delete()
    keyboard = await get_welcome_keyboard(user)
    await callback.message.answer(WELCOME, reply_markup=keyboard)
