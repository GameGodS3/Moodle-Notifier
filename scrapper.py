import json
import os
from api.moodleConnection import MoodleConnection

from dotenv import load_dotenv


def scrape() -> dict:
    load_dotenv()
    username = os.getenv("MOODLEUSERNAME")
    password = os.getenv("MOODLEPASSWD")
    moodle_session = MoodleConnection(username, password)
    home_page_response = moodle_session.login()
    home_page_content = home_page_response.text
    course_list = moodle_session.get_course_list(home_page_content)
    course_dump = {}

    for i in course_list:
        for subject_name, subject_link in i.items():
            [modules, assignments, pdfs, pages, videos] = moodle_session.get_content(
                subject_link)
            content = {
                "Module": modules,
                "Assignment": assignments,
                "PDF": pdfs,
                "Page Link": pages,
                "Video": videos
            }
        course_dump[subject_name] = content

    with open("courseContents.json", "w") as f:
        json.dump(course_dump, f)

    return course_dump
