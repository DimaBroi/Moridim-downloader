import json
import logging
import time

from globals import Conf_ini, Wish_json, Globals
import ConfigParser
from rssMonitor.RssMonitor import RssMonitor
from utilities import call_repeatedly
from wishJsonMgr import WishJsonMgr

def main():
    load_config()
    init_logger()
    logger = logging.getLogger("main")
    logger.debug("logger initialized")
    Wish_json.wishJsonMgr = WishJsonMgr()
    logger.debug("wish json loaded")

    monitor = RssMonitor("https://www.moridim.tv/rss")
    monitor_stop_func = call_repeatedly(float(Conf_ini.conf.get(Conf_ini.Keys.rss, Conf_ini.Keys.checkInterval)),
                          monitor.monitor)

    time.sleep(5)
    #monitor_stop_func()
    time.sleep(15)

def load_config():
    Conf_ini.conf = ConfigParser.ConfigParser()
    read_ok = Conf_ini.conf.read(Conf_ini.conf_filename)
    if not read_ok:
        #TODO : throw exception
        print(Globals.conf_filename + " wasn't found")


def init_logger():
    logging.basicConfig(filename=Globals.log_filename,
                        level=logging.getLevelName(Conf_ini.conf.get(Conf_ini.Keys.general, Conf_ini.Keys.loggingLevel)),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%y %H:%M:%S')


if __name__ == '__main__':
    main()