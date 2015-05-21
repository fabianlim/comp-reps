# some hacking to flesh out ideas on searching equivalent comp graphs

from sympy import reduced, groebner, var
from re import match
import time


# range_var
def range_var(l, robj):
    " populate a range of variates "
    return var(','.join([l+str(i) for i in robj]))


# str_poly
def str_poly(p):
    # convinience function to print out the string representation of a
    # sympy.Poly object
    try:
        return match('Poly\((.*?),', str(p)).group(1)
    except TypeError:
        return ""


# builder
def search_routine(function, initial_node, extensions,
                   num_initial_Y_assigned=1,
                   num_initial_Y_variates=lambda x: len(x[0].free_symbols),
                   groebner_routine=lambda f, G: reduced(f, G, *G.gens)):
    """
        This routine searches through a tree hierachy of comp representations.
        function: the function you want to compute
    """

    # search
    def search(H, n, m):
        """ H: array of polys
            n: number of Y variates already assigned
            m: number of Y variates
        """

        # the groebner_routine *reduced* computes the remainder
        # compute the remainder wrt to a Groebner basis (GB)
        # GB uses lex monomial ordering here, with y's ordered higher than x's
        # this will cause the y's to be eliminated first
        _, rem = groebner_routine(
            function, groebner(H, *range_var('y', range(1, m+1, 1))))

        if rem == 0:
            # return this
            yield [n, m] + [str_poly(h) for h in H] + ["rem: "+str_poly(rem)]

        # if extensions are no more possible
        if n == m:
            return

        # idea: next expression should be chosen to move the groebner basis
        # remainder to zero
        # TODO: of course would be more efficient to update the groebner basis
        # rather than recomputing from scratch each time
        try:
            for h, nn, mm in extensions(H, n, m, rem=rem):
                # h  : new constraint to be enforced
                # nn : update of number of Y variates assigned
                # mm : update of number of Y variates in total
                for g in search(H + [h], nn, mm):  # recurse into search
                    yield g
        except TypeError as e:
            print e
            pass  # for loop will barf if extensions return None

    # return
    return search(initial_node, num_initial_Y_assigned,
                  num_initial_Y_variates(initial_node))


# time_helper
# just run a routine once, recording its ouput and timing it
def time_helper(routine, *args):
    start = time.time()
    out = routine(*args)
    end = time.time()
    return out, end-start
