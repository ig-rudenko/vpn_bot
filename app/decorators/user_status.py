from functools import wraps

from aiogram.types import Message, CallbackQuery

from ..models import User


async def _answer_text(request: Message | CallbackQuery, text: str):
    if isinstance(request, Message):
        await request.answer(text)
    elif isinstance(request, CallbackQuery):
        await request.message.answer(text)
        await request.answer()


def superuser_required(handler):
    @wraps(handler)
    async def wrapper(request: Message | CallbackQuery, *args, **kwargs):
        try:
            user = await User.get(tg_id=request.from_user.id)
        except User.DoesNotExists:
            await _answer_text(request, "Нет доступа")
            return
        else:
            if user.is_superuser:
                await handler(request, *args, **kwargs)
            else:
                await _answer_text(request, "Нет доступа")

    return wrapper
