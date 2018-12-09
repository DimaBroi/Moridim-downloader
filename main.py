#####################################
# Libraries Used in this file       #
#####################################

# Used for log's
import logging
# Used for configuration file hooks
import configparser
# errno used for error handling, sys used for system functions
import errno, sys
# globals is a local configuration for declaring all sorts of constants
from globals import Conf_ini, Wish_json, Globals
# Used for working with rss feeds, RssMonitor is for monitoring the rss feed
from rssMonitor.RssMonitor import RssMonitor
# Used for all sorts of utilitis, call_repeatedly is to run a function every XXX seconds
from utilities import call_repeatedly
# Used for Working with the Json file
from wishJsonMgr import WishJsonMgr

#####################################
# Definition of the main program    #
#####################################

def main():

    # Error handling
    try:
        load_config() # Call the load_config function and load all the configurations
        init_logger() # Initialize the logger system
        logger = logging.getLogger("main") # Create an instance of logger, by using the log "main"
        logger.debug("logger initialized") # Logging a message ("logger initialized") in the log file with level "debug"
        Wish_json.wishJsonMgr = WishJsonMgr() # Create an instance of wishjsonmgr into Wish_Json.wishJsonMgr
        logger.debug("wish json loaded") # Logging a message ("wish json loaded") in the log file with level "debug"
    except Exception as e: # Handle all exceptions and pass them as e (Will be used at later time to handle exceptions)
        #logger.error(str(e)) # (??? is it needed or not ???)
        sys.exit(errno.EPERM) # Exit the program with the error "operation not permitted" (=="EPREM")

    ##########################################
    # Start of the real work for the program #
    ##########################################

    # Create an instance of the RSSMonitor with the link of moridim_rss from the globals file
    monitor = RssMonitor(Globals.moridim_rss)
    # Make repeating calls for the rss monitor while passing the following parameters from the globals file:
    #   Conf_ini.Keys.rss == the RSS feed name
    #   Conf_ini.Keys.checkInterval == the time between calls of the function
    #   monitor.monitor is the function to run under the instance of rss monitor created earlier
    # Pass the all thing to "monitor_stop_func" instance (for later use)
    monitor_stop_func = call_repeatedly(float(Conf_ini.conf.get(Conf_ini.Keys.rss, Conf_ini.Keys.checkInterval)),
                                        monitor.monitor)
    monitor.monitor # (??? why use this call, for what ???

    # ??? Do we need all this ???
    #time.sleep(5)
    #monitor_stop_func()
    #time.sleep(15)



#############################################
# Definition of the load_config function    #
#############################################

def load_config():
    # Create an instance of configuration parser as Conf_ini.conf
    Conf_ini.conf = configparser.ConfigParser()
    # Check the configuration by reading it and insert the result to read_ok
    read_ok = Conf_ini.conf.read(Conf_ini.conf_filename)
    # if the config file read didn't work then print "'config file name' wasn't fond"
    # Needs to throw exceprion and write to the log file
    if not read_ok:
        #TODO : throw exception
        print(Globals.conf_filename + " wasn't found") # ** The Conf_filename is Under Conf_ini, Need to be fixed



#############################################
# Definition of the init_logger function    #
#############################################

def init_logger():
    # Set the basic configuration of to logger with the following parameters:
    # filename: sourced from the globals file using the log_filename parameter
    # level (the level of logging to show in the log):
    #       Conf_ini.Keys.general is holding the section to read from the config file
    #       Conf_ini.Keys.loggingLevel is holding the value to read
    # format is used for formating the log line:
    #       first is the time ascending
    #       then the name of the log ("main")
    #       then the level of the log ("debug")
    #       finally the message itself
    # datefmt is the format of the date to use
    logging.basicConfig(filename=Globals.log_filename,
                        level=logging.getLevelName(Conf_ini.conf.get(Conf_ini.Keys.general, Conf_ini.Keys.loggingLevel)),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%y %H:%M:%S')




#################################################################################
# Check if the file is the main of the program, and if so run the main function #
#################################################################################

if __name__ == '__main__':
    main()