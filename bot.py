import asyncio
import json
import logging
import os
import sys
from datetime import datetime

import pandas as pd
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
DAYS = ("Today", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
BATCH = ("A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3")
df = pd.read_excel(os.getenv("TIMETABLE_FILE"))
mess = pd.read_excel(os.getenv("MENU_FILE"))
meals = [1, 10, 21, 27, 35]
chat_ids = json.load(open("chat_ids.json"))
dp = Dispatcher(storage=MemoryStorage())
shorts = json.load(open("shorts.json"))
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
day_map = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}
builder = InlineKeyboardBuilder()
for index in DAYS:
    builder.button(text=f"{index}", callback_data=f"{index}")
builder.adjust(3, 3)

batch_inline_kb = InlineKeyboardBuilder()
for i in BATCH:
    batch_inline_kb.button(text=f"{i}", callback_data=f"{i}")
batch_inline_kb.adjust(3, 3, 3)


class Form(StatesGroup):
    day = State()
    batch = State()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(
        f"Hello, {hbold(message.from_user.full_name)}!, Use /timetable command to get your today timetable"
    )


@dp.message(Command("timetable"))
async def timetable(message: types.Message, state: FSMContext) -> None:
    today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%A")
    await state.set_state(Form.day)
    await message.answer(
        f"Choose Your Day, Today is {today}", reply_markup=builder.as_markup()
    )


@dp.callback_query(Form.day)
async def filter_batch(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "Today":
        day = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%A")[:3]
    else:
        day = callback_query.data[:3]
    await state.update_data(day=day)
    await state.set_state(Form.batch)
    await bot.edit_message_text(
        "Chose your batch",
        callback_query.from_user.id,
        callback_query.message.message_id,
        reply_markup=batch_inline_kb.as_markup(),
    )


def get_todays_classes(batch, default_batch, today=None):
    if not today:
        today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%A")[:3]
    row_indices = df.index[df.iloc[:, 0] == today].tolist()
    if row_indices:
        row_index = row_indices[0]
        todays_classes = df.iloc[row_index : row_index + 3, :].dropna(how="all")
    else:
        todays_classes = pd.DataFrame()
    todays_classes = todays_classes.apply(
        lambda x: x.map(
            lambda y: y if batch in str(y) or default_batch in str(y) else None
        )
    )
    return todays_classes


def get_venue_course_code(subject, batch):
    if ";" in subject:
        subject = subject.split(";")
        for i in subject:
            if batch in i:
                course_code = i.strip()[:6]
                venue = i.strip()[-3:]
                return course_code, venue
    course_code = subject.strip()[:6]
    venue = subject.strip()[-3:]
    return course_code, venue


@dp.callback_query(Form.batch)
async def send_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    day = data.get("day")
    batch = callback_query.data
    default_batch = f"({batch[0]})"
    todays_classes = get_todays_classes(batch, default_batch, day)
    message = ""
    for _, row in todays_classes.iterrows():
        for time, subject in row.items():
            if pd.notna(subject):
                # The index contains the time and the value is the subject
                course_code, venue = get_venue_course_code(subject, batch)
                if "LT" in venue:
                    subject = shorts[0][course_code]
                else:
                    subject = shorts[1][course_code]
                message += f"Time: {time}, Subject: {subject}, Venue: {venue}\n"
    if len(message) == 0:
        message += "You have no class today \n"
    message += f"Timetable for {batch} for {day}\n"
    message += "Get other timetable by using /timetable \n"
    message += "Created by @aashil \n"
    await bot.edit_message_text(
        message, callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.send_message(
        "-1001670718446",
        f"{hbold(callback_query.from_user.full_name)} \n {callback_query.from_user.id} \n @{callback_query.from_user.username} \n {batch} \n {day}",
    )


def get_menu(day_menu, j):
    return mess.iloc[meals[j] + 1 : meals[j + 1], day_map[day_menu]].dropna(how="all")


async def mess_bot(chat_ids, time: int):
    part = ["Breakfast", "Lunch", "Snacks", "Dinner"]
    day_today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%A")
    today_menu = get_menu(day_today, int(time))
    message_menu = ""
    for j, item in enumerate(today_menu):
        message_menu += f"{j + 1} {item} \n"
    message_menu += f"{part[time]} Menu for {day_today} \n"
    message_menu += "Created By @aashil"
    for k in chat_ids:
        await bot.send_message(chat_id=k, text=message_menu)


@dp.message(Command("add_me"))
async def add_me(message: types.Message):
    if message.from_user.id in chat_ids:
        await message.reply("You are already added")
        return
    chat_ids.append(message.from_user.id)
    with open("chat_ids.json", "w") as f:
        json.dump(chat_ids, f)
    await message.reply("You have been added successfully")


@dp.message(Command("rm_me"))
async def rm_me(message: types.Message):
    if message.from_user.id not in chat_ids:
        await message.reply("You are already removed")
    chat_ids.remove(message.from_user.id)
    with open("chat_ids.json", "w") as f:
        json.dump(chat_ids, f)
    await message.reply("You have been  removed successfully")


async def main() -> None:
    scheduler = AsyncIOScheduler()
    tz = pytz.timezone("Asia/Kolkata")
    trigger_breakfast = CronTrigger(hour=0, minute=2, timezone=tz)
    trigger_lunch = CronTrigger(hour=0, minute=2, timezone=tz)
    trigger_snacks = CronTrigger(hour=0, minute=2, timezone=tz)
    trigger_dinner = CronTrigger(hour=0, minute=2, timezone=tz)
    scheduler.add_job(mess_bot, trigger=trigger_breakfast, args=[chat_ids, 0])
    scheduler.add_job(mess_bot, trigger=trigger_lunch, args=[chat_ids, 1])
    scheduler.add_job(mess_bot, trigger=trigger_snacks, args=[chat_ids, 2])
    scheduler.add_job(mess_bot, trigger=trigger_dinner, args=[chat_ids, 3])
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
