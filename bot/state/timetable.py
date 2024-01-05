from aiogram.fsm.state import State, StatesGroup


class Timetable(StatesGroup):
    day = State()
    batch = State()
