import os
import sys

import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    sys.exit("No token provided")
TIMETABLE_PATH = os.getenv("TIMETABLE_FILE")
ADMIN = tuple(map(int, os.getenv("ADMIN").split(",")))
