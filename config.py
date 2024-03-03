import os
import sys

import dotenv
import pandas as pd
from aiogram import Bot
from aiogram.enums import ParseMode

dotenv.load_dotenv()

ADMIN = tuple(map(int, os.getenv("ADMIN").split(",")))
MESS_FILE = os.getenv("MESS_FILE")
RD_API_TOKEN = os.getenv("RD_API_TOKEN")
TIMETABLE_PATH = os.getenv("TIMETABLE_FILE")
TOKEN = os.getenv("BOT_TOKEN")
host = os.getenv("HOST")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
if not TOKEN:
    sys.exit("No token provided")
mess = pd.read_excel(MESS_FILE)
