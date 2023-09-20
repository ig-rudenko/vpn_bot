from aiogram import types, Router, F
from app.xray.service import xray_service
from ..decorators.user_status import superuser_required

from ..models import User
from app.handlers.welcome import get_welcome_keyboard

router = Router()


@router.callback_query(F.data == "xray")
@superuser_required
async def xray_control(callback: types.CallbackQuery):
    user = await User.get(tg_id=callback.from_user.id)
    status = "Сервис XRAY"
    await xray_service.check_status()

    if xray_service.is_running():
        status += " запущен 🟢\n"
    else:
        status += " не в работе 🔴\n"

    status += f"Потребление памяти: {xray_service.get_memory()}\n"

    await callback.message.edit_text(status, reply_markup=await get_welcome_keyboard(user))
    await callback.answer()
