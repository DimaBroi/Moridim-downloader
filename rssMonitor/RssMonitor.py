import re
import urllib

import feedparser
from bs4 import BeautifulSoup

from globals import Conf_ini, Wish_json
import logging
from functools import reduce
from utilities import encodeUrl


class RssMonitor:
    logger = logging.getLogger(__name__)

    def __init__(self, rss_link):
        self.rss_link = rss_link
        print(Conf_ini.conf.get(Conf_ini.Keys.rss, Conf_ini.Keys.lastUpdateTime))

    def monitor(self):
        updates = feedparser.parse(self.rss_link)

        def look_for_wanted(output, current):
            found_reg = list(filter(lambda reg: re.match(reg, current['title'].split('|')[1].strip()),
                           Wish_json.wishJsonMgr.getKeys()))
            if found_reg:
                # We assume we have on match tops - may need to re-think
                output[found_reg[0]] = encodeUrl(current['links'][1]['href'])
            return output

        found = reduce(look_for_wanted, updates['entries'], {})

        req = urllib.request.Request(encodeUrl(found[list(found.keys())[0]]), headers={'User-Agent': 'Mozilla/5.0'})
        movie_page = urllib.request.urlopen(req).read()
        bs_obj = BeautifulSoup(movie_page, "html.parser")

        for li in bs_obj.find_all("li", {"id": re.compile("release-")}):
            print("==================")
            print(li)
            print("-------------------")
            print(li.a)
            print("==================")
