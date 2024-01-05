from datetime import datetime

import pytz
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot.keyboard.inline import batch_kb
from bot.state.timetable import Timetable
from bot.utils.timetable import timetable_message

callback_router = Router()


@callback_router.callback_query(Timetable.day)
async def filter_batch(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "Today":
        day = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%A")[:3]
    elif callback_query.data:
        day = callback_query.data[:3]
    else:
        await callback_query.message.edit_text("Invalid Input")
        return
    await state.update_data(day=day)
    await state.set_state(Timetable.batch)
    await callback_query.message.edit_text(
        "Chose your batch", reply_markup=batch_kb.as_markup()
    )


@callback_router.callback_query(Timetable.batch)
async def send_timetable(callback_query: types.CallbackQuery, state: FSMContext):
    batch = callback_query.data
    data = await state.get_data()
    day = data.get("day")
    await callback_query.message.edit_text(timetable_message(day, batch))
