import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot import main_router
from config import TOKEN

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(main_router)
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
