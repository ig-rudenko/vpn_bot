from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..decorators.user_status import register_required
from ..service.utils import generate_qr_code
from ..service.vpn import VPNConnectionService
from ..models import User, Profile
from .welcome import cmd_start

router = Router()


@router.callback_query(F.data == "tariff_selection")
@register_required
async def tariff_selection(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Пробная версия",
            callback_data="tariff_selection:trial:info",
        ),
        types.InlineKeyboardButton(
            text="Платная версия",
            callback_data="register",
        ),
    )
    await callback.message.answer(
        "Выберите тариф для подключения",
        reply_markup=builder.as_markup(),
    )
    await callback.answer()


@router.callback_query(F.data == "tariff_selection:trial:info")
@register_required
async def tariff_selection(callback: types.CallbackQuery):
    user = await User.get(tg_id=callback.from_user.id)
    profile = await Profile.get(id=user.profile)

    vpn_connections = await VPNConnectionService.get_connections(profile=profile)
    if len(vpn_connections) > 0:
        await callback.message.answer(
            "У вас уже есть пробное подключение, доступно только одно"
        )
        await cmd_start(callback.message)

    else:
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text="Получить",
                callback_data="tariff_selection:trial:get",
            ),
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="tariff_selection",
            ),
        )
        await callback.message.edit_text(
            "Вам будет предоставлена пробная версия VPN в течение 30 дней",
            reply_markup=builder.as_markup(),
        )
    await callback.answer()


@router.callback_query(F.data == "tariff_selection:trial:get")
@register_required
async def tariff_selection(callback: types.CallbackQuery):
    user = await User.get(tg_id=callback.from_user.id)

    available_to = datetime.now() + timedelta(days=30)
    connection_str = await VPNConnectionService.create_new_connection(
        profile=user.profile,
        username=callback.from_user.username,
        available_to=available_to,
    )
    qr_code: bytes = generate_qr_code(connection_str)
    image = types.BufferedInputFile(qr_code, filename="connection.jpg")
    await callback.message.answer_photo(
        photo=image, caption=f"Подключение было создано\n\n<code>{connection_str}</code>", parse_mode="HTML"
    )
    await callback.answer()
