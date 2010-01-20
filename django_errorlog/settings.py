# -*- coding:utf-8 -*-

## Settings for creating default handlers for loggers. This is deprecated
## in favor of setting up handlers in a project manually.

# Filename for logging one-line exception values
EXCEPTION_LOG_FILE = ''

# Filename for logging full tracebacks
TRACEBACK_LOG_FILE = ''

# Log format
LOGGING_FORMAT = '%(asctime)s %(name)-15s %(levelname)s %(message)s'

# Log file rotation settings
LOGGING_MAX_FILE_SIZE = 1024*1024
LOGGING_MAX_FILES_COUNT = 10
