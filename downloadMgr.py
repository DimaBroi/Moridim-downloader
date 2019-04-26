from lxml import html
import logging
from bs4 import BeautifulSoup
import requests
from pySmartDL import SmartDL
from nitrobitPsw import NitrobitPsw
from globals import Conf_ini, Wish_json
from telegramToken import TelegramToken
import telegram

from wishJsonMgr import WishJsonMgr


class downloadMgr:
    logger = logging.getLogger(__name__)
    list = None

    def __init__(self, download_list):
        self.list = download_list

    def download(self, blocking=False):
        session_requests = requests.session()

        login_url = "https://www.nitrobit.net/login"
        result = session_requests.get(login_url)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='token']/@value")))[0]
        print(authenticity_token)
        payload = {
            "email": NitrobitPsw.email,
            "password": NitrobitPsw.psw,
            "login": "",
            "token": authenticity_token
        }
        session_requests.post(login_url, data=payload)

        def __download_file__(name, url):
            result = session_requests.get(url, headers=dict(referer=url))
            bsObj = BeautifulSoup(result.content, "html.parser")
            li_list = bsObj.find_all("a", {"id": "download"})
            if li_list:
                for li in li_list:
                    dest = Conf_ini.conf.get(Conf_ini.Keys.download, Conf_ini.Keys.downloadPath)+"\\"+name+"\\" #TODO: add support for Linux
                    url = li['href']
                    obj = SmartDL(url, dest, progress_bar=False, logger=self.logger)
                    obj.start(blocking)
                    wishJsonMgr = WishJsonMgr()
                    if Wish_json.Keys.series == wishJsonMgr.getType(name):
                        name += " S"+str(WishJsonMgr.getSeason(name)).zfill(2) \
                                + " E" + str(WishJsonMgr.getEpisode(name)).zfill(2)

                    telegram.Bot(TelegramToken.token).sendMessage(chat_id=433591874, text='Just finished downloading '
                                                                                           + name)
            else:
                logging.error("No download link for " + name + "were found, please check that your user name and password are correct, and make sure you subscription is still valid")

        for name, link in self.list.items():
            __download_file__(name, link)

if __name__ == '__main__':
    downloadMgr({}).download()
