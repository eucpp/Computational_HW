import sys
import os
from sympy import *
from sympy.mpmath import e

x = Symbol('x')
t = Symbol('t')

def f_range(a, b, d):
    while a < b + d:
        yield a
        a += d

def print_row(k, eps, row, out):
    if k == -1:
        out.write('  {:^4}  |'.format('k'))
        out.write('{indent}{num:^15}{indent}|'.format(indent=' '*4, num='eps'))
        for i in range(0, len(row)):
            out.write('{indent}{num:^15}{indent}|'.format(indent=' '*4, num='x'+str(i)))
        out.write(os.linesep)
        return

    out.write('  {:4}  |'.format(k))
    out.write('{indent}{num:+15.12f}{indent}|'.format(indent=' '*4, num=float(eps)))
    for el in row:
        out.write('{indent}{num:+15.12f}{indent}|'.format(indent=' '*4, num=float(el)))
    out.write(os.linesep)

def update_err(x_range, row, func):
    a, b, h = x_range
    xs = [func.subs(x, xi) for xi in f_range(a, b, h)]
    errs = [abs(z - y) for (z, y) in zip(xs, row)]
    return max(errs)

def explicit_method(u, f, a, b, N, K, out):

    h = float(b - a) / N
    tau = h**2 / 2

    psi_1 = u.subs(x, a)
    psi_2 = u.subs(x, b)
    u0    = u.subs(t, 0)

    coefs = zeros(N+1, N+1)
    for i in range(1, N):
        coefs[i, i-1] = tau / h**2
        coefs[i, i]   = 1 - 2*tau / h**2
        coefs[i, i+1] = tau / h**2

    u_pr = Matrix(N+1, 1, [u0.subs(x, xi) for xi in f_range(a, b, h)][:N+1])
    print_row(-1, 0, u_pr, out)
    print_row(0, 0, u_pr, out)
    for k in range(1, K):
        fcol = Matrix(N+1, 1, [f.subs([(t, k * tau), (x, xi)]) for xi in f_range(a, b, h)][:N+1])
        fcol *= tau
        fcol[0] = psi_1.subs(t, k * tau)
        fcol[N] = psi_2.subs(t, k * tau)

        u_new = coefs * u_pr + fcol
        err = update_err((a, b, h), u_new, u.subs(t, k * tau))
        print_row(k, err, u_new, out)
        u_pr = u_new

def implicit_method(u, f, a, b, N, K, out):

    h = float(b - a) / N
    tau = h**2 / 2

    psi_1 = u.subs(x, a)
    psi_2 = u.subs(x, b)
    u0    = u.subs(t, 0)

    coefs = zeros(N+1, N+1)
    coefs[0, 0] = coefs[N, N] = 1
    for i in range(1, N):
        coefs[i, i-1] = tau / h**2
        coefs[i, i]   = -1 - 2*tau / h**2
        coefs[i, i+1] = tau / h**2

    usym = [Symbol('u' + str(i)) for i in range(0, N+1)]

    u_pr = Matrix(N+1, 1, [u0.subs(x, xi) for xi in f_range(a, b, h)][:N+1])
    print_row(-1, 0, u_pr, out)
    print_row(0, 0, u_pr, out)
    for k in range(1, K):
        fcol = Matrix(N+1, 1, [(-tau * f - u_pr[i]).subs([(t, k * tau), (x, xi)]) for (i, xi) in zip(range(0, N+1), f_range(a, b, h))])
        fcol[0] = psi_1.subs(t, k * tau)
        fcol[N] = psi_2.subs(t, k * tau)
        coefs = coefs.col_insert(N+1, fcol)

        sol = solve_linear_system(coefs, *usym)
        u_new = [sol[ui] for ui in usym]
        err = update_err((a, b, h), u_new, u.subs(t, k * tau))
        print_row(k, err, u_new, out)
        u_pr = u_new

        coefs.col_del(N+1)



if __name__ == "__main__":

    u = e**(-t/4) * sin(x/2) + e**(-t) * (1 - x**2)

    f = e**(-t) * (1 + x**2)

    a = 0
    b = 1
    N = 10
    K = 100

    print 'Explicit method is performed ...'

    out = open('explicit_method.txt', 'w')
    explicit_method(u, f, a, b, N, K, out)

    print 'Implicit method is performed ...'

    out = open('implicit_method.txt', 'w')
    implicit_method(u, f, a, b, N, K, out)





