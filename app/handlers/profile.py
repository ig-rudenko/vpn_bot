from typing import Sequence

from aiogram import Router, types
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..decorators.user_status import register_required
from ..service.utils import generate_qr_code
from ..text import VPN_CONNECTION_ATTENTION
from ..xray.generator import xray_connection_maker
from ..helpers import get_user
from ..models import VPNConnection


router = Router()


class GetConnectionCallbackFactory(CallbackData, prefix="vpn_connection"):
    conn_id: int


def get_to_profile_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Назад", callback_data="profile")]
        ]
    )


def get_connections_text_and_buttons_builder(
    connections: Sequence[VPNConnection],
) -> tuple[str, InlineKeyboardBuilder]:
    builder = InlineKeyboardBuilder()
    text = ""
    for conn in connections:
        text += f"Подключение для @{conn.username}\n"
        if conn.is_active:
            text += f"❇️Доступно до: {conn.available_to.strftime('%d %B %Y %H:%M')}\n"
            builder.row(
                types.InlineKeyboardButton(
                    text=f"⚙️Получить конфиг {conn.id}",
                    callback_data=GetConnectionCallbackFactory(conn_id=conn.id).pack(),
                )
            )
        else:
            text += "❌ Подключение больше недоступно!\n"
        text += "\n"

    return text, builder


@router.callback_query(F.data == "profile")
@register_required
async def profile(callback: types.CallbackQuery):
    user = await get_user(callback.from_user.id)

    text = (
        f"Добро пожаловать в профиль!\n"
        f"Ваш username: {user.profile.username}\n"
        f"Профиль был создан: {user.profile.date_joined.strftime('%d %B %Y %H:%M')}\n\n"
    )

    connection = await VPNConnection.filter(profile=user.profile.id)

    go_back_button = types.InlineKeyboardButton(text="Назад", callback_data="start")

    if not connection:
        await callback.message.edit_text(
            text + "У вас нет подключений",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[go_back_button]]),
        )
    else:
        conn_text, keyboard_builder = get_connections_text_and_buttons_builder(
            connection
        )
        keyboard_builder.row(go_back_button)
        await callback.message.edit_text(
            text + conn_text, reply_markup=keyboard_builder.as_markup()
        )

    await callback.answer()


@router.callback_query(GetConnectionCallbackFactory.filter())
@register_required
async def get_config(
    callback: types.CallbackQuery,
    callback_data: GetConnectionCallbackFactory,
):
    user = await get_user(callback.from_user.id)
    try:
        conn: VPNConnection = await VPNConnection.get(
            id=callback_data.conn_id, profile=user.profile.id
        )
    except VPNConnection.DoesNotExists:
        await callback.message.edit_text(
            "Подключение отсутствует!", reply_markup=get_to_profile_keyboard()
        )
    else:
        conn_str = xray_connection_maker.get_connection_string(conn.uuid, conn.username)
        qr_code: bytes = generate_qr_code(conn_str)
        image = types.BufferedInputFile(qr_code, filename="connection.jpg")

        await callback.message.answer_photo(
            photo=image,
            caption=f"Подключение \n\n<code>{conn_str}</code>",
            parse_mode="HTML",
        )
        await callback.message.answer(
            VPN_CONNECTION_ATTENTION, reply_markup=get_to_profile_keyboard()
        )

    await callback.answer()
