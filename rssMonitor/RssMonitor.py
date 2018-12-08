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

    @property
    def monitor(self):
        updates = feedparser.parse(self.rss_link)
        # pars the RSS file:
        def look_for_wanted(output, current):
            found_reg = list(filter(lambda reg: re.match(reg, current['title'].split('|')[1].strip()),
                                    Wish_json.wishJsonMgr.getKeys()))

            if found_reg:
                # We assume we have on match tops - may need to re-think
                if Wish_json.wishJsonMgr.getType(found_reg[0]) == Wish_json.Keys.series:
                    # if we are looking on series we need to check the wanted season and episode
                    if re.match(".*S{:02}E{:02}".format(Wish_json.wishJsonMgr.getSeason(found_reg[0]),
                                                      Wish_json.wishJsonMgr.getEpisode(found_reg[0])),
                                current['title'].split('|')[1].strip()):
                        output[found_reg[0]] = encodeUrl(current['links'][1]['href'])
            return output

        found = reduce(look_for_wanted, updates['entries'], {})
        if not bool(found):
            self.logger.debug("No match found")
            return
        self.logger.debug(str(found))

        # at this point found holds a dictionary/map of name to link string  , the movie/series page at moridim
        def get_bs_object(page_link):
            req = urllib.request.Request(page_link, headers={'User-Agent': 'Mozilla/5.0'})
            movie_page = urllib.request.urlopen(req).read()
            bs_obj = BeautifulSoup(movie_page, "html.parser")
            return bs_obj

        found = {k: get_bs_object(v) for k, v in found.items()}

        # at this point found holds a dictionary/map of name bto of the moridim page
        def get_download_link(page_bs_obj, name):
            if Wish_json.wishJsonMgr.getType(name) == Wish_json.Keys.series:

                #here we find all the li tags, and filter only the one that has the wanted data-season and data-episode

                # TODO: try to use only bs4, it looks overkill
                page_bs_obj = list(filter(lambda li: li.find_all("h4", {"data-season": Wish_json.wishJsonMgr.getSeason(name),
                                                                        "data-episode": Wish_json.wishJsonMgr.getEpisode(name)},
                                                                 recursive=False)
                                     , page_bs_obj.find_all("li")))
                page_bs_obj = page_bs_obj[0]

            #we filterind over the movie/series quality
            for li in page_bs_obj.find_all("li", {"id": re.compile("release-")}):
                quality = li.find_all("b")[1]
                if quality.string in Wish_json.wishJsonMgr.getWantedQuality(list(found.keys())[0]):
                    return li.a["href"]

        found = {k: get_download_link(v, k) for k, v in found.items()}
        found = {k: v for k, v in found.items() if v is not None}

        if not bool(found):
            return

        downloadMgr(found).download(False)

        for name in found.keys():
            if Wish_json.wishJsonMgr.getType(name) == Wish_json.Keys.movies:
                Wish_json.wishJsonMgr.removeMovieByName(name)

            elif Wish_json.wishJsonMgr.getType(name) == Wish_json.Keys.series:
                Wish_json.wishJsonMgr.setNextEpisode(name)

        Wish_json.wishJsonMgr.writeToFile()