#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyloggers.base import NullLogger
from pyloggers.std_capturer import stdoutcatpure


def chatty_factorial(n):
    if n <= 0:
        print 'Hello, mister zero. Do you know, that 0! is 1???'
        return 1
    print 'Hey, it is mister {}.'\
          ' To compute {}! we compute {}! first'.format(n, n, n-1)
    n_1_fact = chatty_factorial(n-1)
    print 'So, {}! is {}. We can find {}!.'\
          ' It is {}'.format(n-1, n_1_fact, n, n * n_1_fact)
    return n * n_1_fact


@stdoutcatpure(NullLogger())
def silent_factorial(n):
    return chatty_factorial(n)


if __name__ == '__main__':
    print chatty_factorial(5)
    print silent_factorial(5)
