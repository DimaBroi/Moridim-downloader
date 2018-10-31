import logging
import time

from globals import Globals, conf_keys
import ConfigParser
from rssMonitor.RssMonitor import RssMonitor
from utilities import call_repeatedly

def main():
    load_config()
    init_logger()
    logger = logging.getLogger("main")
    logger.debug("logger initialized")

    monitor = RssMonitor("https://www.moridim.tv/rss")
    monitor_stop_func = call_repeatedly(float(Globals.conf.get(conf_keys.rss, conf_keys.checkInterval)),
                          monitor.monitor)

    time.sleep(5)
    #monitor_stop_func()
    time.sleep(15)

def load_config():
    Globals.conf = ConfigParser.ConfigParser()
    read_ok = Globals.conf.read(Globals.conf_filename)
    if not read_ok:
        #TODO : throw exception
        print(Globals.conf_filename + " wasn't found")


def init_logger():
    logging.basicConfig(filename=Globals.log_filename,
                        level=logging.getLevelName(Globals.conf.get('General', 'loggingLevel')),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%y %H:%M:%S')

if __name__ == '__main__':
    main()