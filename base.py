#!/usr/bin/python
# -*- coding: utf-8 -*-


class NullLogger(object):
    def __init__(self):
        pass

    def push(self, string, flush=True):
        if flush:
            self.flush()
        return self

    def flush(self):
        return self


class PrintLogger(NullLogger):
    def __init__(self):
        import sys
        self.fo = sys.stdout

    def push(self, string, flush=True):
        self.fo.write(string)
        self.fo.write('\n')
        if flush:
            self.flush()
        return self

    def flush(self):
        self.fo.flush()
        return self


class FileLogger(NullLogger):
    def __init__(self, filename):
        self.fo = open(filename, 'w')

    def push(self, string, flush=False):
        self.fo.write(string)
        self.fo.write('\n')
        if flush:
            self.flush()
        return self

    def flush(self):
        self.fo.flush()
        return self

    def __del__(self):
        self.fo.close()
