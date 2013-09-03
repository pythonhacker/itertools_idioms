# -- coding: utf-8

""" Useful idioms by composing itertools functions.

    License: BSD3 (See LICENSE file)
"""

import random
import itertools
import string
import operator
import functools
import collections

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

    >>> prices = {'cake': 50, 'bread': 20, 'pie': 100}
    >>> constraints = {'cake': (operator.lt, 60), 'bread': (operator.le, 20), 'pie': (operator.lt, 80)}
    >>> list(select(prices,constraints))
    ['cake', 'bread']
    >>> constraints = {'cake': ('less', 60), 'bread': ('less', 30), 'pie': ('lessorequal', 80)}
    >>> cmap = {'less': operator.lt, 'lessorequal': operator.le}
    >>> list(select(prices,constraints, cmap=cmap))  
    ['cake', 'bread']
    >>> constraints = {'cake': ('<', 60), 'bread': ('<=', 20), 'pie': ('<', 80)}
    >>> list(select(prices,constraints, use_operator=True))
    ['cake', 'bread']
    
    """

    s, c, m = subjects, constraints, cmap
    if use_operator:
        m = __operators__
    if m:
        selectors = {key: m[c[key][0]](s[key], c[key][1]) for key in subjects}
    else:
        selectors = {key: c[key][0](s[key], c[key][1]) for key in subjects}
        
    return itertools.compress(selectors.keys(), selectors.values())

def select2(subjects, constraints):
    """ Return iterable from subjects matching the given constraints.
    Both are dictionaries sharing the same keys. Constraints should
    be expressed as a dictionary containing values that are
    functions which take the value(s) of the subject dictionary
    as argument and return a boolean value.

    >>> prices = {'cake': 50, 'bread': 20, 'pie': 100}
    >>> constraints = {'cake': lambda x: x<60,
    ...                'bread': lambda x: x<=20,
    ...                'pie': lambda x: x<80 }
    >>> list(select2(prices, constraints))
    ['cake', 'bread']
    
    """

    s, c = subjects, constraints
    selectors = {key: c[key](value) for key,value in subjects.iteritems()}
    return itertools.compress(selectors.keys(), selectors.values())

def call(callable, *args, **kwargs):
    """ Call a callable with arguments 'args' a given number
    of times. If optional 'times' argument is not passed, returns
    an infinite iterator on the callable with arguments.

    The optional 'filter' argument can be used to pass
    a function which would be used to filter the elements
    of the iterable.

    Useful to make an iterator out of callables that vary
    in the output for same input arguments when called at
    different times.
    
    """

    times = kwargs.get('times',-1)
    filter_func = kwargs.get('filter')

    if filter_func:
        return (i for i in itertools.starmap(callable, itertools.repeat(args, times=times)) if filter_func(i))
    else:
        return itertools.starmap(callable, itertools.repeat(args, times=times))

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
