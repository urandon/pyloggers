#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from functools import wraps
from . import base


class StdoutCaptureLogger(base.NullLogger):
    def __init__(self, logger, dual_stdout_logging=True):
        self._stdout = sys.stdout
        self.dual_stdout_logging = dual_stdout_logging
        self.logger = logger
        sys.stdout = self.logger

    def push(self, string, flush=True):
        self.logger.push(string, flush)
        return self

    def flush(self):
        self.logger.flush()
        return self

    def close(self):
        self.logger.close()
        super(StdoutCaptureLogger, self).close(self)

    def __del__(self):
        sys.stdout = self._stdout


def stdoutcatpure(logger):
    def wrapper(f):
        @wraps(f)
        def tmp(*args, **kwargs):
            _stdout = sys.stdout
            sys.stdout = logger
            ret = f(*args, **kwargs)
            sys.stdout = _stdout
            return ret
        return tmp
    return wrapper
