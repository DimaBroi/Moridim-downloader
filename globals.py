##########################################################
# This file is used to store all sorts of configurations #
# Used in:                                               #
#       main.py                                          #
#       wishJsonMgr.py                                   #
#       RssMonitor.py                                    #
##########################################################

#####################################################################
# Used for global settings                                          #
# Globals are used in:                                              #
#   main.py:                                                        #
#           main()                                                  #
#           load_config()                                           #
#           init_logger()                                           #
#                                                                   #
# moridim_main is used for definition of the site uri, Used in:     #
#           moridim_rss in this file only                           #
#      ** ??? should be moved to the ini config file ???            #
#                                                                   #
# moridim_rss is the full link to the rss feed to follow, Used in:  #
#   main.py:                                                        #
#           main()                                                  #
#      ** ??? should be moved to the ini config file ???            #
#                                                                   #
# log_filename is used to define the log file name, Used in:        #
#   main.py:                                                        #
#           init_logger()                                           #
#####################################################################


class Globals:
    moridim_main = "https://www.moridim.biz"
    moridim_rss = moridim_main + "/rss"
    log_filename = "mDownloader.log"


#####################################################################
# Used for configuration manager parameters                         #
# Used in:                                                          #
#   main.py:                                                        #
#           main()                                                  #
#           load_config()                                           #
#           init_logger()                                           #
#   RssMonitor.py:                                                  #
#           RssMonitor class, ??? for a print statment only ???     #
#                                                                   #
# Conf is initialized as empty and then used in:                    #
#   main.py:                                                        #
#           load_config()                                           #
#   RssMonitor.py:                                                  #
#           RssMonitor class, ??? for a print statement only ???    #
#                                                                   #
# To be continued.............
#####################################################################


class Conf_ini:
    conf = None # Initialize tje configuration with blank
    conf_filename = "mDownloader.ini" # Used for the configuration ini file link

    class Keys: # Used to set the name of the configuration sections and keys
        general = "General" # Used for the general section
        loggingLevel = "loggingLevel" # Used for the logging level parameter
        rss = "RSS" # Used for the RSS section
        lastUpdateTime = "lastUpdateTime" #
        checkInterval = "checkInterval"


class Wish_json:
    wishJsonMgr = None
    wanted_filename = "wanted.json"

    class Keys:
        type = "type"
        series = "series"
        movies = "movies"
        name = "name"
