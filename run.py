import os

from dotenv import load_dotenv

from api.moodleConnection import MoodleConnection

load_dotenv()
username = os.getenv("MOODLEUSERNAME")
password = os.getenv("MOODLEPASSWD")

moodle_session = MoodleConnection(username, password)
with open('moodletest.html', 'w') as f:
    f.write(moodle_session.login().text)
