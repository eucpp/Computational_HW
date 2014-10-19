from sys import stdout
from sympy import *

def f_range(a, b, d):
    while a <= b:
        yield a
        a += d

if __name__ == "__main__":

    n = 10

    h = 0.1

    xs   = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    f_xs = [1.614419,
            1.656832,
            1.694888,
            1.728606,
            1.758030,
            1.783225,
            1.804279,
            1.821299,
            1.834414,
            1.843768]

    m = 5

    diffs = []
    diffs.append(f_xs)

    # calculate differences
    for i in range(1, m):
        i_diff      = []
        prev_diff   = diffs[i - 1]
        for j in range(1, len(prev_diff)):
            i_diff.append(prev_diff[j] - prev_diff[j - 1])
        diffs.append(i_diff)

    lens = list()
    for i in range(0, len(diffs)):
        max = 0
        for j in range(0, len(diffs[i])):
            if max < len(str(diffs[i][j])):
                max = len(str(diffs[i][j]))
        lens.append(max + 3)

    # print differences
    for i in range(0, len(diffs[0])):
        stdout.write(str(xs[i]) + '  ')
        for j in range(0, len(diffs)):
            if i < len(diffs[j]):
                stdout.write(str(diffs[j][i]) + ' '*(lens[j] - len(str(diffs[j][i]))))
        stdout.write('\n')

    # interpolation polynomial
    t  = Symbol('t')
    y0 = Symbol('y0')
    y1 = Symbol('y1')
    y2 = Symbol('y2')
    y3 = Symbol('y3')
    y4 = Symbol('y4')
    intr_poly = Poly(y0 + y1 * t + (y2 / 2) * t * (t - 1) + (y3 / 6) * t * (t - 1) * (t - 2)
                     + (y4 / 24) * t * (t - 1) * (t - 2) * (t - 3))


    x1 = 0.171494
    x2 = 0.764488

    sub1 = [(y0, diffs[0][1]),
            (y1, diffs[1][1]),
            (y2, diffs[2][1]),
            (y3, diffs[3][1]),
            (y4, diffs[4][1]),
            (t,  (x1 - xs[1]) / h)]

    sub2 = [(y0, diffs[0][n - 2]),
            (y1, diffs[1][n - 3]),
            (y2, diffs[2][n - 4]),
            (y3, diffs[3][n - 5]),
            (y4, diffs[4][n - 6]),
            (t,  (x2 - xs[8]) / h)]

    p1 = intr_poly.subs(sub1)
    p2 = intr_poly.subs(sub2)

    print " "
    print "       x_1      |       p(x_1)   "
    print "---------------------------------------------------------------------------"
    print "  {:+.9f}  |  {:+.9f}".format(float(x1), float(p1))
    print "---------------------------------------------------------------------------"
    print "       x_2      |       p(x_2)   "
    print "---------------------------------------------------------------------------"
    print "  {:+.9f}  |  {:+.9f}".format(float(x2), float(p2))