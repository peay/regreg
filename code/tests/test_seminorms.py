import numpy as np
import regreg.atoms as A
import regreg.api as rr
import nose.tools as nt

def ac(x,y):
    print x, y
    return nt.assert_true(np.linalg.norm(x-y) <= 1.0e-04 * max([1, np.linalg.norm(x), np.linalg.norm(y)]))

def test_proximal_maps():
    bound = 0.14
    lagrange = 0.13
    shape = 20

    Z = np.random.standard_normal(shape)
    for L in [0.5,1,0.1]:
        for primal, dual in A.conjugate_seminorm_pairs.items():
            p = primal(shape, lagrange=lagrange)
            d = p.conjugate
            yield nt.assert_equal, d, dual(shape, bound=lagrange)
            yield ac, Z-p.proximal(1, Z, 0), d.proximal(1, Z, 0)
            yield ac, p.lagrange_prox(Z, lipschitz=L), Z-d.bound_prox(Z,bound=p.lagrange/L, lipschitz=L)

            # some arguments of the constructor

            nt.assert_raises(AttributeError, setattr, p, 'bound', 4.)
            nt.assert_raises(AttributeError, setattr, d, 'lagrange', 4.)

            nt.assert_raises(AttributeError, setattr, p, 'bound', 4.)
            nt.assert_raises(AttributeError, setattr, d, 'lagrange', 4.)

            loss = rr.quadratic.shift(-Z, coef=0.5*L)
            problem = rr.separable_problem.singleton(p, loss)
            solver = rr.FISTA(problem)
            solver.fit(tol=1.0e-12)

            yield ac, p.proximal(L, Z, 0), solver.composite.coefs

            loss = rr.quadratic.shift(-Z, coef=0.5*L)
            problem = rr.container(loss, p)
            solver = rr.FISTA(problem)
            solver.fit(tol=1.0e-12)

            yield ac, p.proximal(L, Z, 0), solver.composite.coefs

            problem = rr.separable_problem.singleton(d, loss)
            solver = rr.FISTA(problem)
            solver.fit(tol=1.0e-12)
            yield ac, d.proximal(L, Z, 0), solver.composite.coefs
            
            #yield ac, d.proximal_optimum(Z)[1] + np.linalg.norm(Z)**2/2, p.proximal_optimum(Z)[1]

            d = dual(shape, bound=bound)
            p = d.conjugate
            yield nt.assert_equal, p, primal(shape, lagrange=bound)
            yield ac, Z-p.proximal(L, Z, 0), d.proximal(L, Z, 0)
            yield ac, p.lagrange_prox(Z, lipschitz=L), Z-d.bound_prox(Z,bound=p.lagrange/L, lipschitz=1)

    #        yield ac, d.proximal_optimum(Z)[1], p.proximal_optimum(Z)[1] + np.linalg.norm(Z)**2/2

def test_linear_term_proximal():
    bound = 0.14
    lagrange = 0.5
    shape = 20

    Z = np.random.standard_normal(shape)
    W = 0.02 * np.random.standard_normal(shape)
    linq = rr.identity_quadratic(0,0,W,0)

    for primal, dual in A.conjugate_seminorm_pairs.items():
        for L in [0.5,1]:
            p = primal(shape, lagrange=lagrange, quadratic=linq)
            d = p.conjugate
            print p, d
            yield nt.assert_equal, d, dual(shape, bound=lagrange)
            yield ac, p.proximal(L, Z, 0), Z-d.proximal(L, Z, 0)
            yield ac, p.lagrange_prox(Z,lipschitz=L), Z-d.bound_prox(Z,bound=p.lagrange/L, lipschitz=1)
            ##yield ac, d.proximal_optimum(Z)[1] + np.linalg.norm(Z)**2/2, p.proximal_optimum(Z)[1]

            d = dual(shape, bound=bound, quadratic=linq)
            p = d.conjugate
            yield nt.assert_equal, p, primal(shape, lagrange=bound)
            yield ac, p.proximal(L, Z, 0), Z-d.proximal(L, Z, 0)
            yield ac, p.lagrange_prox(Z,lipschitz=L), Z-d.bound_prox(Z,bound=p.lagrange/L, lipschitz=1)
            
            ##        yield ac, d.proximal_optimum(Z)[1], p.proximal_optimum(Z)[1] + np.linalg.norm(Z)**2/2

            loss = rr.quadratic.shift(-Z, coef=0.5*L)
            problem = rr.separable_problem.singleton(p, loss)
            solver = rr.FISTA(problem)
            solver.fit(tol=1.0e-12)

            yield ac, p.proximal(L, Z, 0), solver.composite.coefs
            problem = rr.separable_problem.singleton(d, loss)

            solver = rr.FISTA(problem)
            solver.fit(tol=1.0e-12)
            yield ac, d.proximal(L, Z, 0), solver.composite.coefs

def test_offset_proximal():
    bound = 0.14
    lagrange = 0.5
    shape = 50

    Z = np.random.standard_normal(shape)
    W = 0.02 * np.random.standard_normal(shape)
    for primal, dual in A.conjugate_seminorm_pairs.items():
        p = primal(shape, lagrange=lagrange, offset=W)
        d = p.conjugate
        print p, d
        yield nt.assert_equal, d, dual(shape, bound=lagrange)
        yield ac, Z-p.proximal(1, Z, 0), d.proximal(1, Z, 0)
        #yield ac, d.proximal_optimum(Z)[1] + np.linalg.norm(Z)**2/2, p.proximal_optimum(Z)[1]

        d = dual(shape, bound=bound, offset=W)
        p = d.conjugate
        yield nt.assert_equal, p, primal(shape, lagrange=bound)
        yield ac, Z-p.proximal(1, Z, 0), d.proximal(1, Z, 0)
#        yield ac, d.proximal_optimum(Z)[1], p.proximal_optimum(Z)[1] + np.linalg.norm(Z)**2/2

def test_offset_and_linear_term_proximal():
    bound = 0.14
    lagrange = 0.5
    shape = 50

    Z = np.random.standard_normal(shape)
    W = 0.02 * np.random.standard_normal(shape)
    U = 0.02 * np.random.standard_normal(shape)
    linq = rr.identity_quadratic(0,0,U,0)
    for primal, dual in A.conjugate_seminorm_pairs.items():
        p = primal(shape, lagrange=lagrange, offset=W, quadratic=linq)
        d = p.conjugate
        print p, d
        yield nt.assert_equal, d, dual(shape, bound=lagrange)
        yield ac, Z-p.proximal(1, Z, 0), d.proximal(1, Z, 0)
        #yield ac, d.proximal_optimum(Z)[1] + np.linalg.norm(Z)**2/2, p.proximal_optimum(Z)[1]

        d = dual(shape, bound=bound, offset=W, quadratic=linq)
        p = d.conjugate
        yield nt.assert_equal, p, primal(shape, lagrange=bound)
        yield ac, Z-p.proximal(1, Z, 0), d.proximal(1, Z, 0)
#        yield ac, d.proximal_optimum(Z)[1], p.proximal_optimum(Z)[1] + np.linalg.norm(Z)**2/2

def test_atoms():

    nt.assert_raises(ValueError, rr.l1norm, 40)
    nt.assert_raises(ValueError, rr.l1norm, 40, bound=1, lagrange=1)
    nt.assert_raises(ValueError, rr.l1norm, 40, bound=-1)

    p1 = rr.l1norm(40, lagrange=3)
    p2 = rr.l1norm(40, lagrange=2)
    p3 = rr.l1norm(40, bound=2)
    p4 = rr.l2norm(30, bound=3)
    ps = [p1, p2, p3, p4]

    for i, p in enumerate(ps):
        for j in range(i):
            nt.assert_not_equal(p, ps[j])

    nt.assert_raises(AttributeError, setattr, p4, 'lagrange', 4)
    nt.assert_raises(AttributeError, setattr, p2, 'bound', 4)



