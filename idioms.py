# -- coding: utf-8

""" Idioms using itertools functions

    License: BSD3 (See LICENSE file)
"""

import random
import itertools
import string
import operator

__operators__ = {'>=': operator.ge,
                 '>': operator.gt,
                 '<': operator.lt,
                 '==': operator.eq,
                 '<=': operator.le}

# With random
def random_stream(iterable, sentinel=None):
    """ Return an infinite stream of random items from the iterable.
    Takes optional sentinel argument which if valid, would end the
    iterator when sentinel is reached """

    random.seed()
    if sentinel:
        return itertools.takewhile(lambda x: x != sentinel, itertools.imap(random.choice, itertools.cycle([iterable])))
    else:
        return itertools.imap(random.choice, itertools.cycle([iterable]))

# BEGIN - Specific use cases of random_stream
def random_alphabets(sentinel=None):
    """ Return a stream of random alphabets """

    return random_stream(string.letters, sentinel)

def random_bits():
    """ Return stream of random 1s and 0s """

    return random_stream([1,0])

def random_digits(sentinel=None):
    """ Return stream of random numbers from 0..9 """

    return random_stream(range(0, 10), sentinel)

# END - Specific use cases of random_stream

def select(subjects, constraints, cmap={}, use_operator=False):
    """ Return iterable from subjects matching the given constraints.
    Both are dictionaries sharing the same keys. Constraints
    should expressed as a dictionary with values expressed
    as a 2-tuple with first member as the checking function
    and 2nd member as the value checked against.

    Also takes an optional cmap argument which can be used to
    map constraints to actual functions. This could be useful
    for example when constraints are no expressed as actual
    functions, but function names or strings.

    For comparison operators >,<,>=,<= and ==, implicit support
    is provided. You can pass the argument use_operator as True
    to enable this. The cmap argument is ignored in such case.
    """

    s, c, m = subjects, constraints, cmap
    if use_operator:
        m = __operators__
    if m:
        selectors = {key: m[c[key][0]](s[key], c[key][1]) for key in subjects}
    else:
        selectors = {key: c[key][0](s[key], c[key][1]) for key in subjects}
        
    return itertools.compress(selectors.keys(), selectors.values())
