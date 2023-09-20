import os

import psutil
from aiogram import types, Router, F
from ..decorators.user_status import superuser_required

from app.models import User
from app.handlers.welcome import get_welcome_keyboard
from app.service.utils import format_bytes

router = Router()


def get_icon(percent):
    if percent < 20:
        return "🟢"
    elif percent < 50:
        return "🟡"
    elif percent < 70:
        return "🟠"
    else:
        return "🔴"


def get_memory() -> str:
    """Получаем информацию о нагрузке оперативной памяти"""
    try:
        mem = psutil.virtual_memory()
    except RuntimeError:
        return ""
    else:
        mem_total = mem.total  # Общий объем оперативной памяти в байтах
        mem_used = mem.used  # Использованный объем оперативной памяти в байтах
        mem_percent = mem.percent  # Процент использования оперативной памяти

        return (
            f"{get_icon(mem_percent)} RAM: {mem_percent}%"
            f" ({format_bytes(mem_used)} из {format_bytes(mem_total)} байт)"
        )


def get_swap() -> str:
    """Получаем информацию о swap"""
    try:
        swap = psutil.swap_memory()
    except RuntimeError:
        return ""
    else:
        swap_total = swap.total  # Общий объем swap в байтах
        swap_used = swap.used  # Использованный объем swap в байтах
        swap_percent = swap.percent  # Процент использования swap
        return (
            f"{get_icon(swap_percent)} SWAP: {swap_percent}% "
            f"({format_bytes(swap_used)} из {format_bytes(swap_total)} байт)"
        )


def get_disk_usage() -> str:
    """Получаем информацию о месте на диске"""
    try:
        # Предполагаем, что интересует корневой диск
        disk = psutil.disk_usage(os.path.abspath(os.sep))
    except RuntimeError:
        return ""
    else:
        disk_total = disk.total  # Общий объем дискового пространства в байтах
        disk_used = disk.used  # Использованный объем дискового пространства в байтах
        disk_percent = disk.percent  # Процент использования дискового пространства
        return (
            f"{get_icon(disk_percent)} DISK: {disk_percent}% "
            f"({format_bytes(disk_used)} из {format_bytes(disk_total)} байт)"
        )


@router.callback_query(F.data == "server")
@superuser_required
async def server_control(callback: types.CallbackQuery):
    user = await User.get(tg_id=callback.from_user.id)

    # Выводим информацию в виде текста
    cpu_percent = psutil.cpu_percent(interval=1)
    status = (
        f"{get_swap()}\n{get_memory()}\n{get_disk_usage()}\n"
        f"{get_icon(cpu_percent)} CPU: {cpu_percent}%"
    )

    await callback.message.edit_text(
        status, reply_markup=await get_welcome_keyboard(user)
    )
    await callback.answer()
