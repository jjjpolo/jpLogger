# =============================================================================
# File Name: jpLogger.py
# =============================================================================
# Purpose:          An inherited class of the logging library from the Python 
#                   standard library. It aims to simplify and speed up the
#                   instantiation of a logging object.
#
# Author:           Jose Juan Jaramillo Polo
# Version:          1.1
# Notes:             
# =============================================================================

import logging
from logging.handlers import RotatingFileHandler
import os
import enum

class displayMode(enum.Enum):
    """
    A enum class that represents the display mode of a log file.
    """
    consoleOnly     = 1
    fileOnly        = 2
    fileAndConsole  = 3

class jpLogger(logging.getLoggerClass()):
    """
    An inherited class of the logging library from the Python standard library.
    It aims to simplify the way a logging object is created by including a 
    a handler for displaying logs in the console and in a file as part of its 
    constructor.
    It also includes default values in the constructor as a matter of demo purposes.
    """

    def __init__(self, appName="unknown", logFileName="noName.log", logLevel=logging.DEBUG, logDisplayMode=displayMode.fileAndConsole, maxFiles=5, maxFileSize=5*1024*1024) -> None:
        """
        Instantiate a logging object to simplify and speed up the creation of a
        logging object that includes (or not depending on the logDisplayMode var value) a 
        handler to display the log messages in the console and to log the log 
        messages in a file using a rotating file handler (the rotating file 
        handler allows to store more than one log file and shift their names as
        needed so that .log is the current file and .log.1 is the second latest one).
        This constructor includes a fixed format that fix almost every project's needs.

        Parameters
        ----------
        appName : str, optional
            The name of the app that is calling/instantiating a jpLogger object.
            This var is used as part of the format.
        logFileName : str, optional
            The path (if not included, log file will be created next to this script)
            and the name (mandatory) of the log file.
        logLevel : int, optional
            The level of logging to use.
            Available enum options: logging.INFO, logging.DEBUG, etc.
        logDisplayMode : int, optional
            Specify the output target that could be console of log file.
            Available options come from displayMode enum class.
        maxFiles : int, optional
            The maximum number of log files to be stored and handled by the 
            rotating file handler.
        maxFileSize : int, optional
            The maximum size (in bytes) of the log file before a new one needs to be created.
        """ 
        super().__init__(appName)   # Assigning it a name (reference)

        self.setLevel(logLevel)     # Despite the config (setLevel) of handlers, 
                                    # this controls the general-log-level to be showed 
                                    # All lower levels will be included.      

        if(logDisplayMode == displayMode.consoleOnly) or (logDisplayMode == displayMode.fileAndConsole):
            consoleLogLevel = logLevel 
            #consoleLogFormat = logging.Formatter('%(message)s')
            consoleLogFormat = logging.Formatter('%(asctime)s - %(levelname)s [ref: %(module)s %(funcName)s(%(lineno)d)] - %(message)s')
            consoleLogHandler = logging.StreamHandler()
            consoleLogHandler.setLevel(consoleLogLevel)
            consoleLogHandler.setFormatter(consoleLogFormat)
            self.addHandler(consoleLogHandler)   
            #self.debug('CMD handler has been added successfully!')

        if(logDisplayMode == displayMode.fileOnly) or (logDisplayMode == displayMode.fileAndConsole):
            fileLogLevel = logLevel 
            fileLogFormat = logging.Formatter('%(asctime)s [tickCount: %(msecs)d] [%(processName)s %(process)d] [%(threadName)s %(thread)d] - %(levelname)s [ref: %(module)s %(funcName)s(%(lineno)d)] - %(message)s')
            self.create_directory_from_file_path(logFileName)
            fileLogHandler = RotatingFileHandler(logFileName, mode='a', maxBytes=maxFileSize, 
                                        backupCount=maxFiles, encoding=None, delay=0)
            fileLogHandler.setLevel(fileLogLevel)
            fileLogHandler.setFormatter(fileLogFormat)
            shouldRollOver = os.path.isfile(logFileName)    # Checks if there is a log file (logFileName) already created, 
                                                            # if so the doRollover() method will rotates the files, this
                                                            # we will create a new file on every run and the oldest one will
                                                            # be deleted.
            if shouldRollOver:  # Log file already exists, roll over!
                fileLogHandler.doRollover()
            self.addHandler(fileLogHandler)
            #self.debug('FILE handler has been added successfully!')

            #self.debug('Logger has been initialized successfully!')

    def create_directory_from_file_path(self, file_path):
        """
        Extracts the directory of a path (ignoring the file and its extension)
        and tries to create the directory. 
        Parameters
        ----------
        file_path : str
            The full path of the log file from where this 
            method will take the directory path and try to
            create the directory. 
        """

        # Extract the directory path from the file path
        directory_path = os.path.dirname(file_path)
        if directory_path == "":
            print(f"Logging directory '{directory_path}' does not need to be created. \n")
            return

        # Check if the directory already exists
        if not os.path.exists(directory_path):
            try:
                # Create the directory
                os.makedirs(directory_path)
                print(f"Logging directory '{directory_path}' created successfully. \n")
            except OSError as e:
                print(f"Error creating logging directory '{directory_path}': {e} \n")
        else:
            print(f"Logging directory '{directory_path}' already exists. \n")

if __name__ == "__main__":
    demoLogger = jpLogger("Demo App ", "demoFile.log", logging.DEBUG, displayMode.fileAndConsole, 7, 5*1024*1024)
    demoLogger.info("Demo Logger")
    demoLogger.debug("Demo Logger")
    demoLogger.warning("Demo Logger")
    demoLogger.error("Demo Logger")
    demoLogger.critical("Demo Logger")