from datetime import datetime

import pytz

from bot.utils.database import db
from config import bot, mess

day_map = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}
meals = [1, 10, 21, 27, 35]


async def mess_bot(time: int):
    user_ids = []
    for users in db.list_all_user_id_mess():
        user_ids.append(users.user_id)
    part = ["Breakfast", "Lunch", "Snacks", "Dinner"]
    day_today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%A")
    today_menu = get_menu(day_today, int(time))
    message_menu = ""
    for j, item in enumerate(today_menu):
        message_menu += f"{j + 1} {item} \n"
    message_menu += f"{part[time]} Menu for {day_today} \n"
    message_menu += "Created By @aashil"
    for k in user_ids:
        await bot.send_message(chat_id=k, text=message_menu)


def get_menu(day_menu, j):
    return mess.iloc[meals[j] + 1 : meals[j + 1], day_map[day_menu]].dropna(how="all")
