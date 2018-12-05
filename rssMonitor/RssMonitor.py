import re
import urllib

import feedparser
from bs4 import BeautifulSoup

from downloadMgr import downloadMgr
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
                output[found_reg[0]] = encodeUrl(current['links'][1]['href']).replace("www.moridim.tv","www.moridim01.tv" )
            return output

        found = reduce(look_for_wanted, updates['entries'], {})

        if not found:
            self.logger.debug("No match found")
            return
        print(found)

        def get_bs_object(page_link):
            req = urllib.request.Request(page_link, headers={'User-Agent': 'Mozilla/5.0'})
            movie_page = urllib.request.urlopen(req).read()
            bs_obj = BeautifulSoup(movie_page, "html.parser")
            return bs_obj

        found = {k: get_bs_object(v) for k, v in found.items()}

        def get_download_link(page_bs_obj):
            for li in page_bs_obj.find_all("li", {"id": re.compile("release-")}):
                quality = li.find_all("b")[1]
                if quality.string in Wish_json.wishJsonMgr.getWantedQuality(list(found.keys())[0]):
                    return li.a["href"]

        found = {k: get_download_link(v) for k, v in found.items()}
        found = {k: v for k, v in found.items() if v is not None}

        print(found)
        downloadMgr(found).download()