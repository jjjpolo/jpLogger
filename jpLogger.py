# =============================================================================
# File Name: jpLogger.py
# =============================================================================
# Purpose:          A wrapper class of the logging library from the Python 
#                   standard library. It aims to simplify and speed up the
#                   instantiaton of a logging object.
#
# Author:           Jose Juan Jaramillo Polo
# Version:          1.0
# Notes:             
# =============================================================================

from logging.handlers import RotatingFileHandler    # For better file logs management| RotatingFileHandler instead of FileHandler
import logging, os                                  # Needed to check if a log files was already created before.
import enum

class displayMode(enum.Enum):
    """
    A enum class that represents the display mode of a log file.
    """
    consoleOnly     = 1
    fileOnly        = 2
    fileAndConsole  = 3

class jpLogger():
    """
    A wrapper class of the logging library from the Python standard library.
    It aims to simplify the way a logging object is created by inclding a 
    a handler for displaying logs in console and in a file as part of its 
    constructor.
    It also includes default values in the constructor as a matter of demo purposes.

    """

    def __init__(self, appName="unknown", logFileName = "noName.log", logLevel=logging.INFO, mode=displayMode.fileAndConsole, maxFiles=5, maxFileSize=5*1024*1024) -> None:       
        """
        Instantiate a logging object to simplify and speed up the creation of a
        logging object that includes (or not depending on the mode var value) a 
        handler to display the log messages in the console and to log the log 
        messages in a file using a rotating file handler (the rotating file 
        handler allows to store more than one log file and shift their names as
        needed so that .log is the current file and .log.1 is the second latest one).
        This constructor includes a fixed format that fix almost every project's needs.

        Parameters
        ----------
        appName : str, optional
            The name of the app that is calling/instantianing a jpLogger object.
            This var is used as part of the format.
        logFileName : str, optional
            The path (if not included, log file will be created next to this script)
            and the name (mandatory) of the log file.
        logLevel : int, optional
            The level of logging to use.
            Available enum options: logging.INFO, logging.DEBUG, etc.
        mode : int, optional
            Specify the output target that could be console of log file.
            Availabel options come from displayMode enum class.
        maxFiles : int, optional
            The max number of log files to be stored and handled by the 
            rotating file handler.
        maxFileSize : int, optional
            The maximum size of the log file before a new one needs to be created.
        """
        self.logger = logging.getLogger(appName) # assinging it a name (reference)
        self.logger.setLevel(logLevel)           # Despite the config (setLevel) of handlers, 
                                                 # this controls the general-log-level to be showed 
                                                 # All lower levels will be included.
      
        if(mode == displayMode.consoleOnly) or (mode == displayMode.fileAndConsole):
            #Creating a printer (in cmd) log handler
            logsToShowInaShell = logLevel #all lower levels will be included 
            logsToShowInaShell_handler = logging.StreamHandler()
            logsToShowInaShell_handler.setLevel(logsToShowInaShell)
            shell_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            logsToShowInaShell_handler.setFormatter(shell_format)
            self.logger.addHandler(logsToShowInaShell_handler)   
            self.logger.debug('Logger CMD handler has been initialized successfully!')

        if(mode == displayMode.fileOnly) or (mode == displayMode.fileAndConsole):
            #Creating a log file handler
            logsToInsertInFile = logLevel #all lower levels will be included 
            should_roll_over = os.path.isfile(logFileName)  # Checks if there is a log file (logFileName) already created, 
                                                            # if so it doRollover() method will rotates the files, this
                                                            # we will have a new file on every run and the oldest one will
                                                            # be deleted.
            logsToInsertInFile_handler = RotatingFileHandler(logFileName, mode='a', maxBytes=maxFileSize, 
                                        backupCount=maxFiles, encoding=None, delay=0)
            if should_roll_over:  # log already exists, roll over!
                logsToInsertInFile_handler.doRollover()
            logsToInsertInFile_handler.setLevel(logsToInsertInFile)
            file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            logsToInsertInFile_handler.setFormatter(file_format)
            self.logger.addHandler(logsToInsertInFile_handler)
            self.logger.debug('Logger FILE handler has been initialized successfully!')
    
        #Use this as an example to use the logger
        self.logger.info('Logger has been initialized successfully!')

    
    def debug(self, str):
        self.logger.debug(str)

    def info(self, str):
        self.logger.info(str)

    def error(self, str):
        self.logger.error(str)

    def warning(self, str):
        self.logger.warning(str)

    def critical(self, str):
        self.logger.critical(str)

if __name__ == "__main__":
    demoLogger = jpLogger("Demo App ", "demoFile.log", logging.DEBUG, displayMode.fileAndConsole, 10, 5*1024*1024)
    demoLogger.info("Demo Logger")
    demoLogger.debug("Demo Logger")
    demoLogger.warning("Demo Logger")
    demoLogger.error("Demo Logger")
    demoLogger.critical("Demo Logger")