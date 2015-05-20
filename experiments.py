# experiments

from itertools import combinations, islice
from sympy import Poly
from search_comp_reps import search_routine, range_var, str_poly
from search_comp_reps import time_helper


# pairs
def pairs(a, b):
    " only these polynomial pairs here "
    return ['{} + {}'.format(a, b), '{} - {}'.format(a, b)]


# extensions
def extensions(leaves, g, a, b, num_max_Y_variates=6):
    """ extend the array of polys g
        a: number of Y variates already assigned
        b: number of Y variates
    """

    # the pair type connector
    if b+2 <= num_max_Y_variates:
        # this would
        connector = [[Poly('y{} - y{} - y{}'.format(a+1, b+1, b+2)), a+1, b+2]]
    else:
        connector = []

    # choices of assigning Ya
    choices = ([[Poly('y{} - ({})'.format(a+1, i)), a+1, b]
                for i in leaves] + connector)

    return [x for x in choices if x not in g]


def backtrack(function):
    """ backtrack search
        static assignments of the leaves
    """

    # collate all the x variates in function and store them
    X = [i for i in function.free_symbols if 'x' in str(i)]

    # leaves are just such pairs here
    leaves = X + [i for x in combinations(X, 2) for i in pairs(*x)]

    def ext(*args, **kwargs):

        # not using the rem argument, and pop it because extensions does not
        # use it either
        kwargs.pop("rem")
        return extensions(leaves, *args, **kwargs)

    # call the search
    return search_routine(function, 'y1 - y2 - y3', ext)


def backtrack2(function):
    """ backtrack search
        tries to assign leaves based on the remainder
    """

    def ext(*args, **kwargs):

        # guess which X variates to assigne for leaves.
        # guess that only X variates of the remainder are interesting
        X = [i for i in kwargs.pop("rem").free_symbols if 'x' in str(i)]

        leaves = X + [i for x in combinations(X, 2) for i in pairs(*x)]
        return extensions(leaves, *args, **kwargs)

    # call the search
    return search_routine(function, 'y1 - y2 - y3', ext)


# main
if __name__ == '__main__':

    X = range_var('x', range(1, 5, 1))
    f = Poly('y1 - ({0})'.format('+'.join(X)))
    print "function: {}".format(str_poly(f))

    # "brute force" method
    r, t = time_helper(list, islice(backtrack(f), 0, 50))
    for i in r:
        print i
    print "time = {} secs".format(t)

    # a little "smarter" about choosing combinations but not much speed up
    # TODO: still yet to prove correctness of the so-called "smarter" method
    r, t = time_helper(list, islice(backtrack2(f), 0, 50))
    for i in r:
        print i
    print "time = {} secs".format(t)

    # the first 50 found
    # [3, 3, 'y1 - y2 - y3', '-x3 - x4 + y2', '-x1 - x2 + y3', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x3 + x4 + y2', 'y3 - y4 - y5', '-x1 - x4 + y4', '-x2 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x3 + x4 + y2', 'y3 - y4 - y5', '-x2 - x4 + y4', '-x1 - x4 + y5', 'rem: 0']
    # [3, 3, 'y1 - y2 - y3', '-x1 - x3 + y2', '-x2 - x4 + y3', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x3 + y2', 'y3 - y4 - y5', 'x1 - x4 + y4', '-x1 - x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x3 + y2', 'y3 - y4 - y5', '-x1 - x2 + y4', 'x1 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'x1 - x3 + y2', 'y3 - y4 - y5', '-x1 - x4 + y4', '-x1 - x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'x1 - x3 + y2', 'y3 - y4 - y5', '-x1 - x2 + y4', '-x1 - x4 + y5', 'rem: 0']
    # [3, 3, 'y1 - y2 - y3', '-x2 - x3 + y2', '-x1 - x4 + y3', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x2 - x3 + y2', 'y3 - y4 - y5', '-x2 - x4 + y4', '-x1 + x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x2 - x3 + y2', 'y3 - y4 - y5', 'x2 - x4 + y4', '-x1 - x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x2 - x3 + y2', 'y3 - y4 - y5', '-x1 - x2 + y4', 'x2 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x2 - x3 + y2', 'y3 - y4 - y5', '-x1 + x2 + y4', '-x2 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'x2 - x3 + y2', 'y3 - y4 - y5', '-x2 - x4 + y4', '-x1 - x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'x2 - x3 + y2', 'y3 - y4 - y5', '-x1 - x2 + y4', '-x2 - x4 + y5', 'rem: 0']
    # [3, 3, 'y1 - y2 - y3', '-x1 - x4 + y2', '-x2 - x3 + y3', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x4 + y2', 'y3 - y4 - y5', '-x3 + x4 + y4', '-x2 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x4 + y2', 'y3 - y4 - y5', 'x1 - x3 + y4', '-x1 - x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x4 + y2', 'y3 - y4 - y5', '-x2 - x4 + y4', '-x3 + x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x4 + y2', 'y3 - y4 - y5', '-x1 - x2 + y4', 'x1 - x3 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'x1 - x4 + y2', 'y3 - y4 - y5', '-x1 - x3 + y4', '-x1 - x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'x1 - x4 + y2', 'y3 - y4 - y5', '-x1 - x2 + y4', '-x1 - x3 + y5', 'rem: 0']
    # [3, 3, 'y1 - y2 - y3', '-x2 - x4 + y2', '-x1 - x3 + y3', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x2 - x4 + y2', 'y3 - y4 - y5', '-x3 + x4 + y4', '-x1 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x2 - x4 + y2', 'y3 - y4 - y5', '-x2 - x3 + y4', '-x1 + x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x2 - x4 + y2', 'y3 - y4 - y5', 'x2 - x3 + y4', '-x1 - x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x2 - x4 + y2', 'y3 - y4 - y5', '-x1 - x4 + y4', '-x3 + x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x2 - x4 + y2', 'y3 - y4 - y5', '-x1 - x2 + y4', 'x2 - x3 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x2 - x4 + y2', 'y3 - y4 - y5', '-x1 + x2 + y4', '-x2 - x3 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'x2 - x4 + y2', 'y3 - y4 - y5', '-x2 - x3 + y4', '-x1 - x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'x2 - x4 + y2', 'y3 - y4 - y5', '-x1 - x2 + y4', '-x2 - x3 + y5', 'rem: 0']
    # [3, 3, 'y1 - y2 - y3', '-x1 - x2 + y2', '-x3 - x4 + y3', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x2 + y2', 'y3 - y4 - y5', '-x1 - x3 + y4', 'x1 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x2 + y2', 'y3 - y4 - y5', 'x1 - x3 + y4', '-x1 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x2 + y2', 'y3 - y4 - y5', '-x2 - x3 + y4', 'x2 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x2 + y2', 'y3 - y4 - y5', 'x2 - x3 + y4', '-x2 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x2 + y2', 'y3 - y4 - y5', '-x1 - x4 + y4', 'x1 - x3 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x2 + y2', 'y3 - y4 - y5', 'x1 - x4 + y4', '-x1 - x3 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x2 + y2', 'y3 - y4 - y5', '-x2 - x4 + y4', 'x2 - x3 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 - x2 + y2', 'y3 - y4 - y5', 'x2 - x4 + y4', '-x2 - x3 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 + x2 + y2', 'y3 - y4 - y5', '-x2 - x3 + y4', '-x2 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', '-x1 + x2 + y2', 'y3 - y4 - y5', '-x2 - x4 + y4', '-x2 - x3 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'y2 - y4 - y5', '-x3 + x4 + y3', '-x1 - x4 + y4', '-x2 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'y2 - y4 - y5', '-x3 + x4 + y3', '-x2 - x4 + y4', '-x1 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'y2 - y4 - y5', '-x1 - x3 + y3', 'x1 - x4 + y4', '-x1 - x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'y2 - y4 - y5', '-x1 - x3 + y3', '-x1 - x2 + y4', 'x1 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'y2 - y4 - y5', 'x1 - x3 + y3', '-x1 - x4 + y4', '-x1 - x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'y2 - y4 - y5', 'x1 - x3 + y3', '-x1 - x2 + y4', '-x1 - x4 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'y2 - y4 - y5', '-x2 - x3 + y3', '-x2 - x4 + y4', '-x1 + x2 + y5', 'rem: 0']
    # [5, 5, 'y1 - y2 - y3', 'y2 - y4 - y5', '-x2 - x3 + y3', 'x2 - x4 + y4', '-x1 - x2 + y5', 'rem: 0']

