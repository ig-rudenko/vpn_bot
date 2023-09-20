from aiogram import types, F, Router

from app.decorators.user_status import superuser_required
from app.handlers.welcome import get_welcome_keyboard
from app.models import VPNConnection, User
from app.service.utils import format_bytes
from app.xray.service import xray_service

router = Router()


@router.callback_query(F.data == "clients_control")
@superuser_required
async def clients_control(callback: types.CallbackQuery):
    user = await User.get(tg_id=callback.from_user.id)
    text = "Подключения пользователей\n\n"

    for client in await VPNConnection.all():
        client: VPNConnection
        user_traffic = await xray_service.get_user_traffic(client.username)
        text += (
            f"@{client.username} {'🟢' if client.is_active else '🔴'}\n"
            f"🔼 Загрузка↑ {format_bytes(user_traffic.uplink)}\n"
            f"🔽 Скачивание↓ {format_bytes(user_traffic.downlink)}\n"
            f"🔄 Всего: {format_bytes(user_traffic.uplink+user_traffic.downlink)}\n\n"
        )

    await callback.message.edit_text(
        text, reply_markup=await get_welcome_keyboard(user=user)
    )
