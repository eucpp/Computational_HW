import sys
from sympy import *

x1 = Symbol('x1')
x2 = Symbol('x2')
x3 = Symbol('x3')

def print_iter(iter, x):
    padd = ' '*4
    div = padd + '|' + padd

    print \
        padd + "{:0>2d}".format(iter) + div + \
        "{:+12.8f}".format(float(x[0])) + div + \
        "{:+12.8f}".format(float(x[1])) + div + \
        "{:+12.8f}".format(float(x[2]))

def get_simple_approx(alpha, beta, x):
    return beta + alpha * x

def get_nekrasov_approx(alpha, beta, x):
    n = x.shape[0]
    xk = zeros(n)
    for i in range(0, n):
        for j in range(0, i-1):
            xk[i] += alpha[i, j] * xk[j]
        for j in range(i+1, n):
            xk[i] += alpha[i,j]  * x[j]
        xk[i] += beta[i]
    return xk


def iteration_method(a, b, eps, cb_approx, cb_print):
    nrow = a.shape[0]
    ncol = a.shape[1]
    alpha = zeros(nrow, ncol)

    for i in range(0, nrow):
        for j in range(0, ncol):
            if i == j:
                alpha[i, i] = 0
            else:
                alpha[i, j] = - a[i, j] / a[i, i]

    beta = zeros(nrow, 1)
    for i in range(0, nrow):
        beta[i] = b[i] / a[i, i]

    xk = beta
    xk_1 = cb_approx(alpha, beta, xk)
    cb_print(0, xk)
    cb_print(1, xk_1)

    iter = 1
    diff = [sys.float_info.max]
    while max(diff) > eps and iter < 20:
        xk = xk_1
        xk_1 = cb_approx(alpha, beta, xk)
        cb_print(iter, xk_1)
        diff = [abs(xi1 - xi2) for (xi1, xi2) in zip(xk, xk_1)]
        iter += 1


if __name__ == "__main__":

    a = Matrix([[1, -0.1, 0.1],
                [0, 1, 0.2],
                [0.1, 0.1, 1]])

    b = Matrix([[1, 1.2, 1.2]])
    b = b.T

    system = a.col_insert(3, b)

    pprint(solve_linear_system(system, x1, x2, x3))
    print ' '

    print " Simple approximation: \n"
    iteration_method(a, b, 1e-5, get_simple_approx, print_iter)
    print "\n Nekrasov approximation: \n"
    iteration_method(a, b, 1e-5, get_nekrasov_approx, print_iter)

    pass