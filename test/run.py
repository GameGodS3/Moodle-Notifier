import json
import os

from dotenv import load_dotenv

from api.moodleConnection import MoodleConnection

load_dotenv()
username = os.getenv("MOODLEUSERNAME")
password = os.getenv("MOODLEPASSWD")

moodle_session = MoodleConnection(username, password)

home_page_response = moodle_session.login()
home_page_content = home_page_response.text

# with open('moodletest.html', 'w') as f:
#     f.write(home_page_response.text)

# with open('moodletest.html', 'r') as f:
#     home_page_content = f.read()

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
