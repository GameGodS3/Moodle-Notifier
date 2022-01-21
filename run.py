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
# for i in course_list:
#     for k, v in i.items():
#         print(f"{k}:{v}\n")

# first_subject_link = list(course_list[8].values())[0]
# print(first_subject_link)

# [modules, assignments, resources] = moodle_session.get_content(
#     first_subject_link)

# content = {"Modules": modules,

#            "Assignments": assignments,

#            "Resources": resources
#            }

course_dump = {}


for i in course_list:
    for subject_name, subject_link in i.items():
        [modules, assignments, resources] = moodle_session.get_content(
            subject_link)
        content = {
            "Modules": modules,
            "Assignments": assignments,
            "Resources": resources
        }
    course_dump[subject_name] = content

with open("courseContents.json", "w") as f:
    json.dump(course_dump, f)
