"""Interval certificates for golden-section and conservative Fibonacci search."""
from math import isclose, isfinite, sqrt


def golden(function, a, b, reductions):
    """Exact-comparison teaching search; assumes strict unimodality on [a,b]."""
    if not isfinite(a) or not isfinite(b) or a >= b:
        raise ValueError("finite ordered bounds required")
    if not isinstance(reductions, int) or reductions < 1:
        raise ValueError("a positive integer reduction count is required")
    tau = (sqrt(5) - 1) / 2
    x1, x2 = a + (1 - tau) * (b - a), a + tau * (b - a)
    f1, f2 = function(x1), function(x2)
    count = 2
    for k in range(reductions):
        if not isfinite(f1) or not isfinite(f2):
            raise ValueError("finite function evaluations required")
        if f1 <= f2:
            b = x2
            x2, f2 = x1, f1
            if k + 1 < reductions:
                x1 = a + (1 - tau) * (b - a)
                f1 = function(x1)
        else:
            a = x1
            x1, f1 = x2, f2
            if k + 1 < reductions:
                x2 = a + tau * (b - a)
                f2 = function(x2)
        if k + 1 < reductions:
            count += 1
    return a, b, count


def fibonacci_bracket(function, a, b, index):
    """Stop at the two-unit bracket, before coincident terminal probes.

    Fibonacci convention F0=0,F1=1. The final width is 2*(b-a)/F_index;
    this conservative variant makes no one-unit terminal-width claim.
    """
    if index < 4 or int(index) != index or not a < b:
        raise ValueError("index >= 4 and ordered bounds required")
    values = [0, 1]
    for _ in range(2, index + 1):
        values.append(values[-1] + values[-2])
    left = a + values[index - 2] / values[index] * (b - a)
    right = a + values[index - 1] / values[index] * (b - a)
    fleft, fright = function(left), function(right)
    for remaining in range(index, 3, -1):
        if fleft <= fright:
            b = right
            right, fright = left, fleft
            left = a + values[remaining - 3] / values[remaining - 1] * (b - a)
            fleft = function(left)
        else:
            a = left
            left, fleft = right, fright
            right = a + values[remaining - 2] / values[remaining - 1] * (b - a)
            fright = function(right)
    return a, b, values[index]


if __name__ == "__main__":
    function = lambda x: (x - 1.3) ** 2 + 2
    a, b, count = golden(function, -2, 5, 10)
    tau = (sqrt(5) - 1) / 2
    assert a <= 1.3 <= b and count == 11
    assert isclose(b - a, 7 * tau ** 10)
    assert abs((a + b) / 2 - 1.3) <= (b - a) / 2
    for index in range(4, 13):
        left, right, fib = fibonacci_bracket(function, -2, 5, index)
        assert left <= 1.3 <= right
        assert isclose(right - left, 14 / fib)
    delta, length = 0.001, 1.0
    for _ in range(3):
        length = (length + delta) / 2
    assert isclose(length, delta + (1 - delta) / 8)
    assert isclose(1.9 * (1.9 - 4), -3.99)
    assert 2 * (2 - 4) == -4
    print("golden: evaluations=%d, width=%.9f, midpoint=%.9f" %
          (count, b - a, (a + b) / 2))
    print("dichotomy: 3 reductions, 6 evaluations, width=%.9f" % length)
