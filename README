* Briefly speaking, a *comp representation* is a
    1. Polynomial representation of a *comp graph* (see below).

* A comp graph is a *directed graph* with
    1. Distinguished leaf nodes known as sinks.
    2. Distinguished nodes with only outgoing edges known as sources.
    3. Internal nodes labeled with operations.
    4. Compute a *function* when the sources are populated with data, and
        propagating to the sinks

* We restrict to *comp graphs* that compute multivariate polynomial
    functions, i.e., *comp graphs* that only have the operations "+, -, *"

* Such *comp graphs* with a *single sink*, have a *comp representation* of
    the following sort:
    1. Call the *single sink* y1
    2. Call the sources x1, x2, .. xn (assuming n sources) and call the
        function f(x1, x2, ..., xn).
        - For convinience write x1, x2, ..., xn as X
    3. Let y1, y2, ..., ym denote intermediate quantities of the computation
        f(X), i.e., there exists polynomials g1, g2, ..., gm
        for which one can express
            y1 = g1(y2, y3, ..., ym) = f(X)
            y2 = g2(y3, y4, ..., ym, X)
            y3 = g3(y2, y2, ..., ym, X)
                ...
            ym = gm(y2, y3, ... y{m-1}, X)

* We have the following result:
    Let Y1, Y2, ..., Ym be intedeterminates. Then,
    a set of multivariate polys {g1, g2, ..., gm} is a *comp representation*
    of f(X) iff the remainder of Y1 - f(X) w.r.t the set {Y1-g1, .... Ym-gm}
    is zero.

    remainder=0 => comp rep
        - since remainder=0, we can therefore write
            Y1-f(X) = a1 (Y1 - g1) + a2 (Y2 - g2) + ... + am (Ym - gm)
        - substitute Y1=g1, Y2=g2, ..., Ym=gm gives 0 on the LHS
        - this implies g1 = f(X) from subsitituing Y1=g1 on the RHS and
            equating to the 0 on the LHS

    comp rep => remainder =0
        - Assume the contrary that there is some non-zero remainder r, i.e.,
            assume that
            Y1-f(X) = a1 (Y1 - g1) + a2 (Y2 - g2) + ... + am (Ym - gm) + r
        - Take the intermediate quantities y1=g1, y2=g2, ..., ym=gm and
            substitute for Y1=y1=g1, etc..., this gives
            r' = subst(r, Y1=g1, ...Ym=gm)
        - by virtute that r was a remainder with none of the linear factors
            listed above, then r' cannot be zero
        - but then we get g1 - f(X) is non-zero, which contradicts the fact
            that {g1, g2, ..., gm} was a comp rep of f.
        - Hence our assumption was incorrect and the result proved.

* We perform the search over sets of polys {g1, g2, ..., gm} to
    find *comp reps* of some function f(X) as follows
    1. Consider a search tree where the nodes at level l correspond to
        size-l sets {g1, g2, ..., gl}
    2. parent-child node relationship in search tree by set containment
    3. if Y1 -f(X) as a zero remainder over the set as described above, then
        we have found a *comp rep* of f.

