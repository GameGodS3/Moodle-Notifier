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

first_subject_link = list(course_list[0].values())[0]
print(first_subject_link)

moodle_session.get_assignments(first_subject_link)
