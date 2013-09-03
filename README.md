Itertools Idioms
================

Useful programming idioms with Python itertools.

Usage:

    >>> from itertools_idioms import idioms
    # Select keys using variable constraints
    >>> import operator
    >>> prices = {'cake': 50, 'bread': 20, 'pie': 100}
    >>> constraints = {'cake': (operator.lt, 60), 'bread': (operator.le, 20), 'pie': (operator.lt, 80)}
    >>> list(idioms.select(prices,constraints))
    ['cake', 'bread']

    # Random streams - infinite and constrained
    
    # Infinite random stream from your iterable
    >>> for i in idioms.random_stream(iterable): print i

    # Specific random streaming functions
    # This would keep going forever
    >>> for i in idioms.random_alphabets(): print i

    # This is constrained and stops when it encounters W
    >>> list(idioms.random_alphabets(sentinel='W'))
    ['i', 'o', 'z', 'y', 'd', 'Z', 'Y', 's', 'S', 'O', 'Q']

    # Infinite generator of random digits    
    >>> idioms.random_digits()
    <itertools.imap object at 0xa12f76c>
    
    # Would stop when encountering 8
    >>> list(idioms.random_digits(sentinel=8))
    [4, 2, 3, 2, 9, 5, 9, 3, 7, 7, 5, 5, 3, 5]

