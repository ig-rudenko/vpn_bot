import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.Message | types.CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        logger = logging.getLogger("aiogram")
        if isinstance(event, types.Message):
            user_action = f"command: {data.get('command').command}"
        else:
            user_action = f"callback: {data['event_update'].callback_query.data}"

        logger.info(
            f"LoggingMiddleware: USER: {event.from_user.id} @{event.from_user.username} ACTION: {user_action}"
        )
        return await handler(event, data)
