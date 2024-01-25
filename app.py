import asyncio
import logging
import sys

import pytz
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot import main_router
from bot.scheduler.mess import mess_bot
from models.users import db,Users
from config import bot

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(main_router)


async def main() -> None:
    scheduler = AsyncIOScheduler()
    db.connect()
    db.create_tables([Users], safe = True)
    db.close()
    tz = pytz.timezone("Asia/Kolkata")
    trigger_breakfast = CronTrigger(hour=0, minute=2, timezone=tz)
    trigger_lunch = CronTrigger(hour=0, minute=3, timezone=tz)
    trigger_snacks = CronTrigger(hour=0, minute=4, timezone=tz)
    trigger_dinner = CronTrigger(hour=0, minute=5, timezone=tz)
    scheduler.add_job(mess_bot, trigger=trigger_breakfast, args=[0])
    scheduler.add_job(mess_bot, trigger=trigger_lunch, args=[1])
    scheduler.add_job(mess_bot, trigger=trigger_snacks, args=[2])
    scheduler.add_job(mess_bot, trigger=trigger_dinner, args=[3])
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
