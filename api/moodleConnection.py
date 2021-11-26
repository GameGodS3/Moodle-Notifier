import traceback

import requests
from lxml import html
from requests.models import Response


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
        tree = html.fromstring(self.login_page.text)
        login_token = list(
            set(tree.xpath("//input[@name='logintoken']/@value")))[0]
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
