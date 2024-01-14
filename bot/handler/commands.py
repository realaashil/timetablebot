from datetime import datetime

import pytz
from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.bot_command import BotCommand
from aiogram.utils.markdown import hbold

from bot.keyboard.inline import day_kb
from bot.state.timetable import Timetable
from bot.utils.database import db

commands_router = Router()


@commands_router.message(
    Command(BotCommand(command="start", description="Start the bot"))
)
async def command_start_handler(message: types.Message) -> None:
    db.add_user(message.from_user)
    await message.answer(
        f"Hello, {hbold(message.from_user.full_name)}!, Use /timetable command to get your today timetable"
    )


@commands_router.message(
    Command(BotCommand(command="timetable", description="Send IIIT KOTA Timetable"))
)
async def timetable(message: types.Message, state: FSMContext) -> None:
    today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%A")
    await state.set_state(Timetable.day)
    await message.answer(
        f"Choose Your Day, Today is {today}", reply_markup=day_kb.as_markup()
    )


@commands_router.message(
    Command(BotCommand(command="rm_me", description="remove from mess notification"))
)
async def remove_mess(message: types.Message):
    db.remove_mess(message.from_user.id)
    await message.reply("Removed from mess notification")


@commands_router.message(
    Command(BotCommand(command="add_me", description="add mess notification"))
)
async def add_mess(message: types.Message):
    db.add_mess(message.from_user.id)
    await message.reply("Added to mess notification")
