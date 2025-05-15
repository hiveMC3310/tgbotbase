from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class AdminsMiddleware(BaseMiddleware):
    def __init__(self, admins: list[int]):
        self.admins = admins

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        data["admins"] = self.admins
        return await handler(event, data)
