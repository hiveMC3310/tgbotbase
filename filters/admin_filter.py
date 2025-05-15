from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class IsAdminFilter(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery, admins: list[int]) -> bool:
        user = getattr(event, "from_user", None)
        return user is not None and user.id in admins
