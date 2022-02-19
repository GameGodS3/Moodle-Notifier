import json
import os
from api.moodleConnection import MoodleConnection

from dotenv import load_dotenv


def scrape() -> list:
    """
    Scrape the moodle course list and return a dict with the courses
    """
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
            print(f"Scraping {subject_name}...")
            [modules, assignments, pdfs, pages, videos] = moodle_session.get_content(
                subject_link)
            content = {
            }
            if modules:
                content["module"] = modules
            if assignments:
                content["assignment"] = assignments
            if pdfs:
                content["pdf"] = pdfs
            if pages:
                content["page"] = pages
            if videos:
                content["video"] = videos
        # course_dump[subject_name] = content
        course_dump.update({course_list.index(i): {subject_name: content}})

        # Remove all empty key value pairs in course dump
        # course_dump_clean = {k: v for k, v in course_dump.items() if v}

    course_dump = [v for k, v in course_dump.items()]
    # print(course_dump)

    with open("courseContents.json", "w") as f:
        json.dump(course_dump, f)

    return course_dump
