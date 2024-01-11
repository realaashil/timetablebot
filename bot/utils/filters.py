from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from config import ADMIN


class IsAdmin(BaseFilter):
    async def __call__(self, obj: CallbackQuery | Message) -> bool:
        return obj.from_user.id in ADMIN
