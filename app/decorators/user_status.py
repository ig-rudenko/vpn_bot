from functools import wraps

from aiogram.types import Message, CallbackQuery

from ..models import User


async def _answer_text(request: Message | CallbackQuery, text: str):
    if isinstance(request, Message):
        await request.answer(text)
    elif isinstance(request, CallbackQuery):
        await request.message.answer(text)


def register_required(handler):
    @wraps(handler)
    async def wrapper(request: Message | CallbackQuery, *args, **kwargs):
        try:
            user = await User.get(tg_id=request.from_user.id)
        except User.DoesNotExists:
            await _answer_text(request, "Начните с команды /start")
            return
        else:
            if user.profile is not None:
                await handler(request, *args, **kwargs)
            else:
                await _answer_text(
                    request,
                    "Вам необходимо зарегистрироваться либо войти\nНачните с команды /start",
                )

    return wrapper
