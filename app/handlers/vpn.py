from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..decorators.user_status import register_required
from ..service.utils import generate_qr_code
from ..service.vpn import VPNConnectionService
from ..models import User, Profile
from .welcome import get_welcome_keyboard

router = Router()


async def get_user(tg_id: int) -> User:
    user = await User.get(tg_id=tg_id)
    profile = await Profile.get(id=user.profile)
    user.profile = profile
    return user


async def check_trial(user: User, callback: types.CallbackQuery) -> bool:
    if user.profile.trial_count < 1:
        keyboard = await get_welcome_keyboard(callback.from_user.id)
        await callback.message.answer(
            "У вас закончились пробные подключения", reply_markup=keyboard
        )
        await callback.answer()
        return False
    return True


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
    user = await get_user(callback.from_user.id)

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
@register_required
async def tariff_selection(callback: types.CallbackQuery):
    user = await get_user(callback.from_user.id)

    if not await check_trial(user, callback):
        return

    available_to = datetime.now() + timedelta(days=30)
    connection_str = await VPNConnectionService.create_new_connection(
        profile=user.profile,
        username=callback.from_user.username,
        available_to=available_to,
    )
    await user.profile.update(trial_count=user.profile.trial_count - 1)

    qr_code: bytes = generate_qr_code(connection_str)
    image = types.BufferedInputFile(qr_code, filename="connection.jpg")
    await callback.message.answer_photo(
        photo=image,
        caption=f"Подключение было создано\n\n<code>{connection_str}</code>",
        parse_mode="HTML",
    )
    await callback.answer()
