# some hacking to flesh out ideas on searching equivalent comp graphs

from sympy import reduced, Poly, groebner
from itertools import combinations
from re import match


# range_var
def range_var(l, robj):
    " populate a range of variates "
    return [l+str(i) for i in robj]


# str_poly
def str_poly(p):
    # convinience function to print out the string representation of a
    # sympy.Poly object
    try:
        return match('Poly\((.*?),', str(p)).group(1)
    except TypeError:
        return ""


# backtrack
def backtrack(function, X, num_max_Y_variates=6):
    """
        This routine searches through a tree hierachy of comp representations.
        function: the function you want to compute
        X: set of X variates
    """

    # polys (shortcut)
    def pairs(a, b):
        " will only consider these polynomial pairs for now "
        return ['{} + {}'.format(a, b), '{} - {}'.format(a, b)]

    leaves = [i for x in combinations(X, 2) for i in pairs(*x)]

    # extensions
    def extensions(g, a, b):
        """ extend the array of polys g
            a: number of Y variates already assigned
            b: number of Y variates
        """

        # choice of Y
        if b+2 <= num_max_Y_variates:
            # this would
            connector = [[Poly('y{} - y{} - y{}'.format(b, b+1, b+2)), a, b+2]]
        else:
            connector = []

        # choices of assigning Ya
        choices = ([[Poly('y{} - ({})'.format(a+1, i)), a+1, b]
                   for i in leaves] + connector)

        return [x for x in choices if x not in g]

    # search
    def search(H, n, m):
        """ H: array of polys
            n: number of Y variates already assigned
            m: number of Y variates
        """

        # the routine *reduced* computes the remainder
        # compute the remainder wrt to a Groebner basis (GB)
        # GB uses lex monomial ordering here, with y's ordered higher than x's
        # this will cause the y's to be eliminated first
        _, rem = reduced(
            function, groebner(list(H), wrt=range_var('y', range(1, m+1, 1))))
        if rem == 0:
            print [n, m] + [str_poly(h) for h in ([rem] + H)]
            return

        # idea: next expression should be chosen to move the groebner basis
        # remainder to zero
        # TODO: of course would be more efficient to update the groebner basis
        # rather than recomputing from scratch each time
        try:
            for h, nn, mm in extensions(H, n, m):
                # h  : new constraint to be enforced
                # nn : update of number of Y variates assigned
                # mm : update of number of Y variates in total
                if nn < mm:
                    search(H + [h], nn, mm)  # recurse into search
        except TypeError:
            pass  # for loop will barf if extensions return None

    # call the search algorithm
    # initialize with the 3 node graph y2 <- y1 -> y3
    # y1 is already assigned ( will be assigned y1 = graph )
    search([Poly('y1 - y2 - y3')], 1, 3)

# main
if __name__ == '__main__':

    X = range_var('x', range(1, 5, 1))
    function = Poly('y1 - ({0})'.format('+'.join(X)))
    print "function: {}".format(str_poly(function))

    backtrack(function, X)  # run the backtrack
