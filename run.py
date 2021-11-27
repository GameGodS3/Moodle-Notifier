import os

from dotenv import load_dotenv

from api.moodleConnection import MoodleConnection

load_dotenv()
username = os.getenv("MOODLEUSERNAME")
password = os.getenv("MOODLEPASSWD")

moodle_session = MoodleConnection(username, password)

home_page_response = moodle_session.login()

with open('moodletest.html', 'w') as f:
    f.write(home_page_response.text)

course_list = moodle_session.course_list(home_page_response)
print(course_list)
