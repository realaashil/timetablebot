import json
import re
from datetime import datetime

import pandas as pd
import pytz

from config import TIMETABLE_PATH

df = pd.read_excel(TIMETABLE_PATH)
course_name = json.load(open("./static/course_name.json"))


def get_todays_classes(batch, today=None):
    if not today:
        today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%A")[:3]
    row_indices = df.index[df.iloc[:, 0] == today].tolist()
    if row_indices:
        row_index = row_indices[0]
        section_indice = df.iloc[int(row_index) : int(row_index) + 3, 1].index[
            df.iloc[int(row_index) : int(row_index) + 3, 1] == f"II Sem {batch[0]}"
        ]
        todays_classes = df.iloc[section_indice, :].dropna(how="all")
    else:
        todays_classes = pd.DataFrame()
    todays_classes = todays_classes.apply(
        lambda x: x.map(lambda y: y if batch in str(y) or "LT" in str(y) else None)
    )
    return todays_classes


def timetable_message(day: str, batch: str) -> str:
    todays_classes = get_todays_classes(batch, day)
    message = ""
    for _, row in todays_classes.iterrows():
        for time, subject in row.items():
            if pd.notna(subject):
                # The index contains the time and the value is the subject
                subject, venue = get_subject_course_code(subject, batch)
                message += f"Time: {time}, Subject: {subject}, Venue: {venue}\n"
    if len(message) == 0:
        message += "You have no class today \n"
    message += f"Timetable for {batch} for {day}\n"
    message += "Get other timetable by using /timetable \n"
    message += "To get mess menu everyday at 12am use /add_me \n"
    message += "Created by @aashil \n"
    return message


def get_subject_course_code(subject, batch):
    if "/" in subject:
        subject = subject.split("/")
        for i in subject:
            if batch in i:
                course_code = i.strip()[:6]
                subject = course_name[course_code]
                venue = (
                    re.findall(r"\[(.*?)\]", i)[0]
                    if re.findall(r"\[(.*?)\]", i)
                    else "Venue Not Found"
                )
                return subject, venue
    venue = (
        re.findall(r"\[(.*?)\]", subject)[0]
        if re.findall(r"\[(.*?)\]", subject)
        else "Venue Not Found"
    )
    course_code = subject.strip()[:6]
    subject = course_name[course_code]
    return subject, venue
