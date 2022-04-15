# What is _jpLogger_ ?
This is only a wrapper of the logging library from the Python standard library. It aims to provide an easy way to get a mechanism to log messages, errors, and so on. 
This is a personal implementation that fits a frequent need that I have every time I work on a Python project. It also might fit other users' needs, so that is why I decided to make it public.

# What does it include?
* It is a class so the instance can be passed to any place as needed. 
* A console logging handler to show logs in the console as if they were print statements.
* A rotating log file: This means that you can store more than one log file (the latest log), and every time a new one is created, the rotating file handler will shift the current (latest one) to be the .1 extension and so son. 
* Maximum file size can be set so that the rotating file system will automatically create a new one once the current reaches the maximum size.
* A logging format already set that fits almost every need.

# How to use it.
1. Import this script from your project.
```
from jpLogger import *
```
2. Create a jpLogger instance.
```
# Using default values:
demoLogger = jpLogger()

# jpLogger instance with custom values:
demoLogger = jpLogger(appName="demo", logFileName = "demo.log", logLevel=logging.INFO, mode=displayMode.cmdAndLog, maxFiles=5, maxFileSize=5*1024*1024)
```
3. Printing logs.
```
demoLogger.info("Demo Logger")
demoLogger.debug("Demo Logger")
demoLogger.warning("Demo Logger")
demoLogger.error("Demo Logger")
demoLogger.critical("Demo Logger")
```

# References
## In case you need more info about Logging and its handlers in Python.
* [Logging facility for Python](https://docs.python.org/3/library/logging.html).
* [Logging handlers](https://docs.python.org/3/library/logging.handlers.html?highlight=rotating#logging.handlers.RotatingFileHandler).
* [Python: How to Create Rotating Logs](https://www.blog.pythonlibrary.org/2014/02/11/python-how-to-create-rotating-logs/).
* [Logger configuration to log to file and print to stdout](https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout).