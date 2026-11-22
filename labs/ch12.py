"""Penalty limits, barrier gaps, and valid convex cuts."""
import json
import math

import numpy as np
from scipy.optimize import linprog


def main():
    parameters = [.1, 1., 10., 100.]
    exterior = [5 - 1 / (2 * rho) for rho in parameters]
    inverse_barrier = [5 + math.sqrt(mu) for mu in parameters]
    log_barrier = [5 + mu for mu in parameters]
    assert all(x < 5 for x in exterior)
    assert all(x > 5 for x in inverse_barrier + log_barrier)
    assert np.isclose(exterior[-1], 4.995)
    assert np.isclose(log_barrier[0], 5.1)
    # Minimize -x on x^2 <= 1, starting with the outer box [-2, 2].
    rows, rhs, iterates = [], [], []
    for _ in range(20):
        result = linprog([-1.], A_ub=rows or None, b_ub=rhs or None,
                         bounds=[(-2., 2.)], method='highs', options={
                             'primal_feasibility_tolerance': 1e-10,
                             'dual_feasibility_tolerance': 1e-10})
        assert result.success
        x = result.x[0]
        iterates.append(float(x))
        if x * x - 1 <= 1e-9:
            break
        # x_k^2 - 1 + 2*x_k*(x-x_k) <= 0.
        rows.append([2 * x])
        rhs.append(x * x + 1)
    assert np.allclose(iterates[:3], [2, 1.25, 1.025])
    assert abs(iterates[-1] - 1) < 1e-8
    # Tangency alone does not make a straight step feasible on a curved set.
    point, direction = np.array([1., 0.]), np.array([0., 1.])
    assert np.dot(2 * point, direction) == 0
    assert np.linalg.norm(point + .01 * direction) ** 2 > 1
    # At a central-path point for min x, x >= 5, gap = mu.
    mu = .01
    x, multiplier = 5 + mu, 1.
    assert np.isclose(multiplier * (x - 5), mu)
    print(json.dumps(dict(parameters=parameters, exterior=exterior,
                          inverse_barrier=inverse_barrier,
                          logarithmic_barrier=log_barrier,
                          cutting_plane_iterates=iterates)))


if __name__ == '__main__':
    main()
