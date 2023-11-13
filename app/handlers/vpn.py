from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..service.shortcuts import answer_connection_config
from ..service.vpn import VPNConnectionService
from ..models import User
from .welcome import get_welcome_keyboard

router = Router()


async def check_trial(user: User, callback: types.CallbackQuery) -> bool:
    """
    Функция «check_trial» проверяет, есть ли у пользователя оставшиеся пробные подключения,
    и возвращает «True», если они есть, в противном случае она отображает сообщение
    в телеграм и возвращает «False».
    """
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
    """
    Отображает меню с опциями выбора тарифа и отправляет его пользователю в виде сообщения.
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Получить настройки",
            # callback_data="tariff_selection:trial:info",
            callback_data="tariff_selection:trial:get",
        ),
        types.InlineKeyboardButton(
            text="💀 Профиль",
            callback_data="profile",
        ),
        # types.InlineKeyboardButton(
            # text="Платная версия",
            # callback_data="tariff_selection:paid:info",
        # ),
    )
    builder.row(types.InlineKeyboardButton(text="🔙 Назад", callback_data="start"))
    await callback.message.edit_text(
        #"Выберите тариф для подключения",
        "Нажмав \"🔗 Получить настройки\" Вы получите QR-code и ссылку, которая Вам необходима для настройки приложения на Вашем устройстве \n Для просмотра\получения существующих настроек смотрите \n раздел \"💀 Профиль\"",
        reply_markup=builder.as_markup(),
    )
    await callback.answer()


# ======================= Пробное подключение =====================


@router.callback_query(F.data == "tariff_selection:trial:info")
async def tariff_selection_trial_info(callback: types.CallbackQuery):
    """
    Функция «tariff_selection_trial_info» отображает пользователю сообщение, информирующее его о том,
    что он получит 30-дневную пробную версию VPN, и предоставляет возможность либо получить пробную версию,
    либо вернуться в предыдущее меню.
    """
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
    """
    Проверяет, имеет ли пользователь право на пробную версию, создает новое
    VPN-соединение и обновляет счетчик пробных версий пользователя.
    """
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
    await answer_connection_config(callback, connection_str)
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
