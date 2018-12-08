from lxml import html
import logging
from bs4 import BeautifulSoup
import requests
from pySmartDL import SmartDL
from globals import Wish_json
from nitrobit_psw import nitrobit_psw


class downloadMgr:
    logger = logging.getLogger(__name__)
    list = None

    def __init__(self, download_list):
        self.list = download_list

    def download(self):
        session_requests = requests.session()

        login_url = "https://www.nitrobit.net/login"
        result = session_requests.get(login_url)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='token']/@value")))[0]
        print(authenticity_token)
        payload = {
            "email": nitrobit_psw.email,
            "password": nitrobit_psw.psw,
            "login": "",
            "token": authenticity_token
        }
        session_requests.post(login_url, data=payload)

        def __download_file__(url):
            result = session_requests.get(url, headers = dict(referer=url))
            bsObj = BeautifulSoup(result.content, "html.parser")
            for li in bsObj.find_all("a",{"id":"download"}):
                dest = "D:\\movies\\auto_movies\\"  # or '~/Downloads/' on linux
                url = li['href']
                obj = SmartDL(url, dest, progress_bar=False, logger=self.logger)
                obj.start(blocking=False)

        for name in self.list.keys():
            Wish_json.wishJsonMgr.removeMovieByName(name)
        Wish_json.wishJsonMgr.writeToFile()

        for name, link in self.list.items():
            __download_file__(link)

if __name__ == '__main__':
    downloadMgr({}).download()