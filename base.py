#!/usr/bin/python
# -*- coding: utf-8 -*-


class NullLogger(object):
    def __init__(self):
        self._is_closed = False
        pass

    def push(self, string, flush=True):
        if flush:
            self.flush()
        return self

    def write(self, string):
        self.push(string)
        return len(string)

    def flush(self):
        pass

    def close(self):
        self._is_closed = True
        self.flush()

    def closed(self):
        return self._is_closed


class PrintLogger(NullLogger):
    def __init__(self):
        import sys
        self.fo = sys.stdout

    def push(self, string, flush=True):
        self.fo.write(string.strip() + "\n")
        if flush:
            self.flush()
        return self

    def flush(self):
        self.fo.flush()


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

    def close(self):
        super(FileLogger, self).close(self)
        self.fo.close()

    def __del__(self):
        self.close()
