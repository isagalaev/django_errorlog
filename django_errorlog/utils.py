# -*- coding:utf-8 -*-
import logging

from django_errorlog.models import _log_exc_info, exception_str

def log_error(exc_info=None):
    '''
    Logs exc_info into 'exception' and 'traceback' logs with ERROR level.
    If exc_info is None get it from sys.exc_info().
    '''
    _log_exc_info(exc_info, level=logging.ERROR)

def log_warning(exc_info=None):
    '''
    Logs exc_info into 'exception' and 'traceback' logs with WARNING level.
    If exc_info is None get it from sys.exc_info().
    '''
    _log_exc_info(exc_info, level=logging.WARNING)

