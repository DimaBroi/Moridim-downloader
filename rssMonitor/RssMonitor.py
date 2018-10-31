from datetime import datetime
import feedparser
from globals import Globals, conf_keys
import logging
import threading
import time

class RssMonitor:
    logger = logging.getLogger(__name__)

    def __init__(self, rss_link, time_interval=10):
        self.rss_link = rss_link
        self.time_interval = time_interval
        print(Globals.conf.get(conf_keys.rss, conf_keys.lastUpdateTime))
        self.last_update_time = datetime.strptime(Globals.conf.get(conf_keys.rss, conf_keys.lastUpdateTime),
                                                  '%Y-%m-%d %H:%M:%S')

    def monitor(self):
        print(time.ctime())
        print (self.last_update_time)
        updates = feedparser.parse(self.rss_link)
        for entry in updates['entries']:
            datetime_object = datetime.strptime(entry['published'].split('GMT')[0], '%a, %d %b %Y %H:%M:%S ')
            if self.last_update_time >= datetime_object:
                break
            print(str(datetime_object) + " - " + entry['title'].split('|')[1][1:])

        last_update_datetime_object = datetime.strptime(updates['entries'][0]['published'].split('GMT')[0], '%a, %d %b %Y %H:%M:%S ')
        if self.last_update_time < last_update_datetime_object:
            self.last_update_time = last_update_datetime_object
