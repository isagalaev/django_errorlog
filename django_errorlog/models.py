# -*- coding:utf-8 -*-
import sys
import os
import re
import traceback
import logging
from logging import handlers
import warnings

import django
from django.core import signals
from django.utils.encoding import smart_str
from django.conf import settings


major, minor, release, stage, _ = django.VERSION
if (major, minor, release, stage) >= (1, 3, 0, 'final'):
    warnings.warn('Django_errorlog is obsolete. Setup logging using standard Django settings', DeprecationWarning)

def _get_logger(name, setting_name):
    '''
    Returns a named logger.

    Creates a default file handler for it if there's a setting for it
    (deprecated).
    '''
    if name not in _get_logger.loggers:
        logger = logging.getLogger(name)
        if getattr(settings, setting_name, ''):
            try:
                handler = handlers.RotatingFileHandler(
                    getattr(settings, setting_name),
                    'a',
                    settings.LOGGING_MAX_FILE_SIZE,
                    settings.LOGGING_MAX_FILES_COUNT
                )
            except:
                handler = logging.StreamHandler(None)
            handler.setFormatter(logging.Formatter(settings.LOGGING_FORMAT))
            logger.addHandler(handler)
        _get_logger.loggers[name] = logger

    return _get_logger.loggers[name]
_get_logger.loggers = {}

def exception_str(value):
    '''
    Formats Exception object to a string. Unlike default str():

    - can handle unicode strings in exception arguments
    - tries to format arguments as str(), not as repr()
    '''
    try:
        return ', '.join([smart_str(b) for b in value])
    except (TypeError, AttributeError): # happens for non-iterable values
        try:
            return smart_str(value)
        except UnicodeEncodeError:
            try:
                return repr(value)
            except Exception:
                return '<Unprintable value>'

POST_TRUNCATE_SIZE = 1024

def format_post(request):
    '''
    Casts request post data to string value. Depending on content type it's
    either a dict or raw post data.
    '''
    if request.method == 'POST' and request.META['CONTENT_TYPE'] not in ['application/x-www-form-urlencoded', 'multipart/form-data']:
        value = request.raw_post_data[:POST_TRUNCATE_SIZE]
        if len(request.raw_post_data) > len(value):
            value += '... (post data truncated at %s bytes)' % POST_TRUNCATE_SIZE
        return value
    else:
        return str(request.POST)

def _log_exc_info(exc_info=None, level=logging.ERROR, aditional_lines=None):
    '''
    Logs exception info into 'exception' and 'traceback' loggers calling
    formatting as necessary.
    '''
    exception, value, tb = exc_info or sys.exc_info()
    exception_logger = _get_logger('exception', 'EXCEPTION_LOG_FILE')
    # find innermost call
    inner = tb
    while inner.tb_next:
        inner = inner.tb_next
    lineno = inner.tb_lineno
    module_name = inner.tb_frame.f_globals.get('__name__', '<unknown>')
    exception_logger.log(level, '%-20s %s:%s %s' % (
        exception.__name__,
        module_name,
        lineno,
        exception_str(value),
    ))

    lines = traceback.format_exception(exception, value, tb)
    if aditional_lines:
        lines = aditional_lines + lines
    traceback_logger = _get_logger('traceback', 'TRACEBACK_LOG_FILE')
    traceback_logger.log(level, '\n'.join([smart_str(l) for l in lines]))

def _log_request_error(sender, request, **kwargs):
    '''
    Handles unhandled request exceptions.
    '''
    lines = [
        'Path: %s' % request.path,
        'GET: %s' % request.GET,
        'POST: %s' % format_post(request),
    ]
    _log_exc_info(aditional_lines=lines)

signals.got_request_exception.connect(_log_request_error)

