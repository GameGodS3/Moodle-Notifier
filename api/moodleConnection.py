from sys import modules
import traceback
from bs4.element import ResultSet

import requests
from requests.models import Response
from bs4 import BeautifulSoup


class MoodleConnection:
    def __init__(self, user: str, pwd: str) -> None:
        self.__user = user
        self.__pwd = pwd
        self.login_page = None
        self.login_url = "http://lms.cet.ac.in/login/index.php"
        self.adaptor = requests.session()

        try:
            self.login_page = self.adaptor.get(self.login_url)
            self.login_page.raise_for_status()
        except requests.exceptions.HTTPError as err:
            traceback.print_exc(err)
            self.adaptor.close()

    def close(self) -> None:
        if self.adaptor is not None:
            self.adaptor.close()

    def login(self) -> Response:
        soup = BeautifulSoup(self.login_page.text, 'html5lib')
        login_token = soup.find('input', attrs={"name": "logintoken"})["value"]
        payload = {
            "anchor": "",
            "username": self.__user,
            "password": self.__pwd,
            "logintoken": login_token
        }

        result = self.adaptor.post(
            self.login_url,
            data=payload,
            headers=dict(referer=self.login_url)
        )

        return result

    def get_course_list(self, home_page_content: str) -> list:
        home_page = BeautifulSoup(home_page_content, 'html5lib')

        course_menu = home_page.find_all('div', {'class': 'ml-1'})

        course_list = []

        for i in course_menu:
            for j in i.strings:
                if '\n' not in j:
                    url = i.parent['href']
                    course_list.append({j: url})

        return course_list

    def get_content(self, course_link: str) -> ResultSet:
        course_page = self.adaptor.get(course_link)
        # with open('coursepage.html', 'w') as f:
        #     f.write(course_page.text)
        course_page_content = course_page.text

        # with open('coursepage.html', 'r') as f:
        #     course_page_content = f.read()

        course_soup = BeautifulSoup(course_page_content, 'html5lib')

        modules_raw = course_soup.find_all('h3', {'class': 'sectionname'})[1:]
        assignments_raw = course_soup.find_all('li', {'class': 'assign'})
        resources_raw = course_soup.find_all('li', {'class': 'resource'})[2:]

        # To find Assignment Names
        assignments = []
        for i in assignments_raw:
            assignments += i.find('span',
                                  {'class': 'instancename'}).stripped_strings
        assignments = assignments[::2]

        # To find Module Names
        modules = []
        for i in modules_raw:
            modules += i.stripped_strings

        # To find Resources Names
        resources = []
        for i in resources_raw:
            resources += i.find('span',
                                {'class': 'instancename'}).stripped_strings
        resources = resources[::2]

        return [modules, assignments, resources]
