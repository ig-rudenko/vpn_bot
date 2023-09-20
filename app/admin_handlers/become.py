from aiogram import types
from aiogram import Router, F

router = Router()


@router.callback_query(F.data == "become")
async def become_admin(callback: types.CallbackQuery, command: types.BotCommand):
    print(command, command.command)
    await callback.answer()
