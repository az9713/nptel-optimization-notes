"""Geometric programming: primal solution and independent dual certificate."""
import json

import numpy as np
from scipy.optimize import minimize


def main():
    # min x + y + 1/(x*y), x,y>0, with x<=1/2 in the constrained case.
    def objective(z):
        x, y = np.exp(z)
        return x + y + 1 / (x * y)

    free = minimize(objective, [1., -1.], method='BFGS',
                    options={'gtol': 1e-7})
    assert np.allclose(np.exp(free.x), [1, 1], atol=1e-6)
    assert np.isclose(free.fun, 3)
    constrained = minimize(objective, [-1., 0.], method='SLSQP',
                           constraints=[dict(type='ineq', fun=lambda z:
                                             -np.log(2) - z[0])],
                           options={'ftol': 1e-12})
    assert constrained.success
    x, y = np.exp(constrained.x)
    value = .5 + 2 * np.sqrt(2)
    assert np.allclose([x, y], [.5, np.sqrt(2)], atol=1e-6)
    assert np.isclose(constrained.fun, value)
    delta = np.array([.5, np.sqrt(2), np.sqrt(2)]) / value
    multiplier = delta[2] - delta[0]
    # Exponent balance: [1,0], [0,1], [-1,-1], [1,0].
    exponents = np.array([[1., 0.], [0., 1.], [-1., -1.], [1., 0.]])
    all_delta = np.r_[delta, multiplier]
    assert np.allclose(exponents.T @ all_delta, 0)
    log_dual = -np.sum(delta * np.log(delta)) + multiplier * np.log(2)
    assert np.isclose(np.exp(log_dual), value)
    assert np.isclose(delta.sum(), 1)
    # A posynomial superlevel set need not be convex in log coordinates.
    a, b = np.log([2., .25]), np.log([.25, 2.])
    midpoint = (a + b) / 2
    assert np.exp(a).sum() >= 2 and np.exp(b).sum() >= 2
    assert np.exp(midpoint).sum() < 2
    print(json.dumps(dict(unconstrained_point=np.exp(free.x).tolist(),
                          unconstrained_value=float(free.fun),
                          constrained_point=[float(x), float(y)],
                          constrained_value=value, dual_weights=delta.tolist(),
                          constraint_weight=float(multiplier),
                          dual_value=float(np.exp(log_dual)))))


if __name__ == '__main__':
    main()
