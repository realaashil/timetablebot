import json
from datetime import datetime

import pandas as pd
import pytz

from config import TIMETABLE_PATH

shorts = json.load(open("./static/course_name.json"))
df = pd.read_excel(TIMETABLE_PATH)


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


def timetable_message(day: str, batch: str) -> str:
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
    return message


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
