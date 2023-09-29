from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .deleter import get_delete_back_button
from ..service.utils import generate_qr_code
from ..service.vpn import VPNConnectionService
from ..models import User
from .welcome import get_welcome_keyboard
from ..text import VPN_CONNECTION_ATTENTION

router = Router()


async def check_trial(user: User, callback: types.CallbackQuery) -> bool:
    if user.trial_count < 1:
        keyboard = await get_welcome_keyboard(user)
        await callback.message.edit_text(
            "У вас закончились пробные подключения", reply_markup=keyboard
        )
        await callback.answer()
        return False
    return True


@router.callback_query(F.data == "tariff_selection")
async def tariff_selection(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Пробная версия",
            callback_data="tariff_selection:trial:info",
        ),
        types.InlineKeyboardButton(
            text="Платная версия",
            callback_data="tariff_selection:paid:info",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="start"
        )
    )
    await callback.message.edit_text(
        "Выберите тариф для подключения",
        reply_markup=builder.as_markup(),
    )
    await callback.answer()


# ======================= Пробное подключение =====================


@router.callback_query(F.data == "tariff_selection:trial:info")
async def tariff_selection_trial_info(callback: types.CallbackQuery):
    user = await User.get_or_create(callback.from_user)

    if not await check_trial(user, callback):
        return

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
async def tariff_selection_trial_get(callback: types.CallbackQuery):
    user = await User.get_or_create(callback.from_user)

    if not await check_trial(user, callback):
        return

    available_to = datetime.now() + timedelta(days=30)
    connection_str = await VPNConnectionService.create_new_connection(
        tg_id=user.tg_id,
        username=callback.from_user.username or str(callback.from_user.id),
        available_to=available_to,
    )
    await user.update(trial_count=user.trial_count - 1)

    qr_code: bytes = generate_qr_code(connection_str)
    image = types.BufferedInputFile(qr_code, filename="connection.jpg")
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=image,
        caption=f"Подключение было создано\n\n<code>{connection_str}</code>\n\n{VPN_CONNECTION_ATTENTION}",
        reply_markup=get_delete_back_button(),
        parse_mode="HTML",
    )
    await callback.answer()


# ======================= ПЛАТНЫЕ ============================


@router.callback_query(F.data == "tariff_selection:paid:info")
async def tariff_selection_paid_info(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Назад",
            callback_data="tariff_selection",
        ),
    )
    await callback.message.edit_text(
        "В данный момент доступны только пробные версии",
        reply_markup=builder.as_markup(),
    )
    await callback.answer()
