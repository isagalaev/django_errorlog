# -*- coding:utf-8 -*-
'''
The application works automatically: it listents for a signal that Django sends
on all uncaught server errors and then logs short exception values and full
tracebacks into their respective log channels.

There are two utility functions in django_errorlog.utils: log_error and
log_warning. They can be used to manually log exception that you do handle in
your code. They accept exc_info (a triple of (exceptions, value, traceback) as
an argument. If called without arguments they get it from sys.exc_info().
'''
