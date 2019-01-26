#####################################
# Libraries Used in this file       #
#####################################


import logging
import configparser
import errno, sys
from globals import Conf_ini, Wish_json, Globals
from rssMonitor.RssMonitor import RssMonitor
from wishJsonMgr import WishJsonMgr

#####################################
# Definition of the main program    #
#####################################

def main():

    # Error handling
    try:
        load_config() 
        init_logger() 
        logger = logging.getLogger("main") 
        logger.debug("logger initialized") 
        Wish_json.wishJsonMgr = WishJsonMgr() 
        logger.debug("wish json loaded") 
    except Exception as e:
        sys.exit(errno.EPERM) 
        
    RssMonitor(Globals.moridim_rss).monitor()

def load_config():
    Conf_ini.conf = configparser.ConfigParser()
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