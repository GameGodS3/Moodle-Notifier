import traceback

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

    def course_list(self, home_page_response: Response) -> list:
        home_page = BeautifulSoup(home_page_response.text, 'lxml')

        course_menu = home_page.find_all('div', {'class': 'ml-1'})

        course_list = []

        for i in course_menu:
            for j in i.strings:
                course_list.append(j)

        course_list = list(filter(lambda a: a != "\n", course_list))

        return course_list
