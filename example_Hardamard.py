# experiments

from itertools import combinations, islice
from sympy import Poly, reduced
from search_comp_reps import search_routine, str_poly
from search_comp_reps import time_helper
from example import pairs, extensions


def backtrack(function):
    """ backtrack search
        vector function version
    """

    def ext(*args, **kwargs):

        # copy out the free symbols
        rem = kwargs.pop("rem")
        fs = rem.free_symbols
        # print fs
        # import pdb
        # pdb.set_trace()
        # if len([i for i in fs if 'y' in str(i)]) == 0:
        if 'y' not in str_poly(rem):
            return []

        # guess which X variates to assigne for leaves.
        # guess that only X variates of the remainder are interesting
        X = [i for i in fs if 'x' in str(i)]

        leaves = X + [i for x in combinations(X, 2) for i in pairs(*x)]
        return extensions(leaves, num_max_Y_variates=12,
                          *args, **kwargs)

    # compute the Y variates assigned in function
    variates = reduce(lambda x, y: x.union(y),
                      [i.free_symbols for i in function])
    Y = sorted([i for i in variates if 'y' in str(i)],
               cmp=lambda x, y: x.compare(y))

    # build the initial node (inode)
    n = len(Y)
    inode = []
    for y in Y:
        s, n = '{} - y{} - y{}'.format(y, n+1, n+2), n+2
        inode.append(Poly(s))

    # groebner routine
    def routine(functions, B):
        for f in functions:
            a, rem = reduced(f, B, *B.gens)
            if rem != 0:
                return _, rem
        return _, Poly(0, *B.gens)

    return search_routine(function, inode, ext,
                          num_initial_Y_assigned=len(inode),
                          num_initial_Y_variates=lambda x: 3*len(inode),
                          groebner_routine=routine)


# main
if __name__ == '__main__':

    print "Example: Hardamard Transform"

    def Hardamard():
        f1 = Poly('x1 + x2 + x3 + x4 - y1')
        f2 = Poly('x1 - x2 + x3 - x4 - y2')
        f3 = Poly('x1 + x2 - x3 - x4 - y3')
        f4 = Poly('x1 - x2 - x3 + x4 - y4')
        return [f1, f2, f3, f4]

    f = Hardamard()
    print "matrix : {}".format([str_poly(i) for i in f])

    r, t = time_helper(list, islice(backtrack(f), 0, 1))
    for i in r:
        print i
    print "time = {} secs".format(t)
