from datetime import datetime
import feedparser
from globals import Conf_ini, Wish_json
import logging
import re

class RssMonitor:
    logger = logging.getLogger(__name__)

    def __init__(self, rss_link):
        self.rss_link = rss_link
        print(Conf_ini.conf.get(Conf_ini.Keys.rss, Conf_ini.Keys.lastUpdateTime))
        self.last_update_time = datetime.strptime(Conf_ini.conf.get(Conf_ini.Keys.rss,
                                                                    Conf_ini.Keys.lastUpdateTime),
                                                  '%Y-%m-%d %H:%M:%S')

    def monitor(self):
        updates = feedparser.parse(self.rss_link)

        # wishes_names = {Wish_json.Keys.movies : map((lambda wish: wish[Wish_json.Keys.name]),
        #                                     Wish_json.wishes[Wish_json.Keys.movies])}

        for entry in updates['entries']:
            datetime_object = datetime.strptime(entry['published'].split('GMT')[0], '%a, %d %b %Y %H:%M:%S ')
            if self.last_update_time >= datetime_object:
                break
            name = entry['title'].split('|')[1][1:]
            matching_regs = filter(lambda reg: re.match(reg, name),
                                   Wish_json.wishJsonMgr.getKeys())
            if len(matching_regs):
                if 2 <= len(matching_regs):
                    self.logger.error( name + " mathces " + str(len(matching_regs)) + "wanted items :" + str(matching_regs))
                    #TODO: send msg to user to take action - for now wwe ignore such rear case.
                print("downloading " + name)
            else:
                print("not downloading " + name)


        last_update_datetime_object = datetime.strptime(updates['entries'][0]['published'].split('GMT')[0], '%a, %d %b %Y %H:%M:%S ')
        if self.last_update_time < last_update_datetime_object:
            self.last_update_time = last_update_datetime_object

