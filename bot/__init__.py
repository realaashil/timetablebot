from aiogram import Router

from bot.handler.callbacks import callback_router
from bot.handler.commands import commands_router

main_router = Router()
main_router.include_router(commands_router)
main_router.include_router(callback_router)

__all__ = ("main_router",)
