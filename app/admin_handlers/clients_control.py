from aiogram import types, F, Router

from app.decorators.user_status import superuser_required
from app.handlers.welcome import get_welcome_keyboard
from app.models import VPNConnection, User
from app.service.utils import format_bytes
from app.xray.service import xray_service

from datetime import datetime

router = Router()


@router.callback_query(F.data == "clients_control")
@superuser_required
async def clients_control(callback: types.CallbackQuery):
    user = await User.get(tg_id=callback.from_user.id)
    text = "Подключения пользователей\n\n"
    user_count = 0
    for client in await VPNConnection.all():
        client: VPNConnection
        user_traffic = await xray_service.get_user_traffic(client.username)
        username_string = client.username if client.username.isdigit() else f"@{client.username}"
        text += (
            f"{username_string} {'🟢' if client.is_active else '🔴'} {datetime.strptime(client.created_datetime, '%d/%m/%Y')}|{datetime.strptime(client.available_to, '%d/%m/%Y')} \n"
            f"🔼{format_bytes(user_traffic.uplink)} "
            f"🔽{format_bytes(user_traffic.downlink)} \n"
            # f"🔄 Всего: {format_bytes(user_traffic.uplink+user_traffic.downlink)}\n\n"
        )
        user_count +=1
    text += (f" Всего пользователей: {user_count}")
    await callback.message.edit_text(
        text, reply_markup=await get_welcome_keyboard(user=user)
    )
