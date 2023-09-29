from typing import Literal

from aiogram import F, Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


async def send_photos(
    message: types.Message,
    system_type: Literal["android", "iphone", "windows"],
    photo_count: int = 3,
):
    return await message.answer_media_group(
        media=[
            types.InputMediaPhoto(
                media=types.FSInputFile(f"media/guide/{system_type}/img_{i}.png")
            )
            for i in range(1, photo_count + 1)
        ]
    )


def get_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="install:info",
        ),
    )
    return builder.as_markup()


@router.callback_query(F.data == "install:info")
async def install_info(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="📱 Android",
            callback_data="install:info:android",
        ),
        types.InlineKeyboardButton(
            text="📱 iPhone",
            callback_data="install:info:iphone",
        ),
        types.InlineKeyboardButton(
            text="💻 Windows",
            callback_data="install:info:windows",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="start",
        ),
    )

    await callback.message.edit_text(
        "Выберите, для какой системы вам необходимо посмотреть инструкцию по установке клиента",
        reply_markup=builder.as_markup(),
    )
    await callback.answer()


@router.callback_query(F.data == "install:info:android")
async def install_info_android(callback: types.CallbackQuery):
    await send_photos(callback.message, "android")
    await callback.message.answer(
        text="Скачайте приложение, затем выберите `+` чтобы добавить новое подключение,"
        " Вы можете скопировать текст подключения и вставить его через буфер обмена,"
        " либо отсканировать QR код. "
        "Также можно сохранить изображение QR кода и выбрать его затем в приложении.\n\n"
        '📱 Для android <a href="https://play.google.com/store/apps/details?id=com.v2ray.ang&hl=ru">скачать</a>',
        reply_markup=get_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "install:info:iphone")
async def install_info_iphone(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text='📱 iPhone <a href="https://apps.apple.com/app/id6450534064">скачать</a>',
        reply_markup=get_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "install:info:windows")
async def install_info_windows(callback: types.CallbackQuery):
    await send_photos(callback.message, "windows", photo_count=7)
    await callback.message.reply(
        text='💻 Windows <a href="https://github.com/InvisibleManVPN/InvisibleMan-XRayClient/releases">скачать</a>',
        reply_markup=get_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()
