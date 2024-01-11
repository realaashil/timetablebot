from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from bot.utils.filters import IsAdmin

admin_router = Router()
admin_router.message.filter(IsAdmin())


@admin_router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello You are a admin!")
