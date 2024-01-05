from aiogram.utils.keyboard import InlineKeyboardBuilder

DAYS = ("Today", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
BATCH = ("A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3")

day_kb = InlineKeyboardBuilder()

for index in DAYS:
    day_kb.button(text=f"{index}", callback_data=f"{index}")

day_kb.adjust(3, 3)

batch_kb = InlineKeyboardBuilder()

for index in BATCH:
    batch_kb.button(text=f"{index}", callback_data=f"{index}")
batch_kb.adjust(3, 3, 3)
