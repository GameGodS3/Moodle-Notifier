import requests
from lxml import html
import os
from dotenv import load_dotenv

load_dotenv()

session_request = requests.session()

login_url = "http://lms.cet.ac.in/login/index.php"
result = session_request.get(login_url)

tree = html.fromstring(result.text)
login_token = list(set(tree.xpath("//input[@name='logintoken']/@value")))[0]

print(f"Result Page:\n-------------------\n{result}")
print(login_token)

session_request = requests.session()

login_url = "http://lms.cet.ac.in/login/index.php"
result = session_request.get(login_url)

tree = html.fromstring(result.text)
login_token = list(set(tree.xpath("//input[@name='logintoken']/@value")))[0]

print(f"Result Page:\n-------------------\n{result}")
# print(login_token)

username = os.getenv("MOODLEUSERNAME")
password = os.getenv("MOODLEPASSWD")

payload = {
    "anchor": "",
    "username": username,
    "password": password,
    "logintoken": login_token
}

result = session_request.post(
    login_url,
    data=payload,
    headers=dict(referer=login_url)
)

with open('moodle.html', 'w') as f:
    f.write(result.text)
