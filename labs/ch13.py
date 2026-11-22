"""Piecewise linear separable optimization, including adjacency checks."""
import itertools
import json

import numpy as np
from scipy.optimize import linprog, minimize


def solve_grid(grid):
    """Globally solve all adjacent cells for the chapter's two-variable model."""
    grid = np.asarray(grid, float)
    if grid.ndim != 1 or len(grid) < 2 or not np.isfinite(grid).all():
        raise ValueError('A finite one-dimensional grid is required')
    if np.any(np.diff(grid) <= 0) or grid[0] != 0 or grid[-1] != 2:
        raise ValueError('Use a strictly increasing grid covering [0, 2]')
    best = None
    for i, j in itertools.product(range(len(grid) - 1), repeat=2):
        nodes = np.r_[grid[i:i + 2], grid[j:j + 2]]
        objective = np.r_[nodes[:2] ** 2 - 4 * nodes[:2], -nodes[2:]]
        resource = np.r_[2 * nodes[:2] ** 2, 8 * nodes[2:] ** 2]
        # The cell LP has fractions alpha,beta in [0,1] and one resource row.
        base = resource[0] + resource[2]
        slopes = np.array([resource[1] - resource[0],
                           resource[3] - resource[2]])
        candidates = [np.array(z, float) for z in itertools.product([0, 1], repeat=2)]
        for axis in range(2):
            other = 1 - axis
            if slopes[axis] != 0:
                for fixed in [0., 1.]:
                    z = np.zeros(2)
                    z[other] = fixed
                    z[axis] = (30 - base - slopes[other] * fixed) / slopes[axis]
                    candidates.append(z)
        for z in candidates:
            if np.any(z < 0) or np.any(z > 1) or base + slopes @ z > 30 + 1e-10:
                continue
            weights = np.array([1 - z[0], z[0], 1 - z[1], z[1]])
            value = float(objective @ weights)
            if best is None or value < best['value']:
                x = [nodes[:2] @ weights[:2], nodes[2:] @ weights[2:]]
                best = dict(value=value, point=x)
    if best is None:
        raise ValueError('No feasible interpolated cell')
    return best


def main():
    coarse = solve_grid([0, 1, 2])
    fine = solve_grid(np.linspace(0, 2, 41))
    assert np.allclose(coarse['point'], [2, 19 / 12])
    assert np.isclose(coarse['value'], -67 / 12)
    # Independent LP reference, valid here because all sampled curves are convex.
    reference = linprog([0, -3, -4, 0, -1, -2],
                        A_ub=[[0, 2, 8, 0, 8, 32]], b_ub=[30],
                        A_eq=[[1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1]],
                        b_eq=[1, 1], bounds=(0, None), method='highs')
    assert reference.success and np.isclose(reference.fun, coarse['value'])
    result = minimize(lambda x: x[0] ** 2 - 4 * x[0] - x[1],
                      [1.8, 1.7], bounds=[(0, 2), (0, 2)],
                      constraints=[dict(type='ineq', fun=lambda x:
                                        30 - 2 * x[0] ** 2 - 8 * x[1] ** 2)],
                      method='SLSQP', options={'ftol': 1e-12})
    assert result.success
    assert 2 * fine['point'][0] ** 2 + 8 * fine['point'][1] ** 2 <= 30 + 1e-8
    assert coarse['value'] >= fine['value'] >= result.fun - 1e-8
    assert fine['value'] - result.fun < .002
    # Nonadjacent interpolation of a concave function invents a lower value.
    nodes = np.array([0., 1., 2.])
    values = -(nodes - 1) ** 2
    weights = np.array([.5, 0., .5])
    assert np.isclose(nodes @ weights, 1)
    assert values @ weights == -1 and values[1] == 0
    print(json.dumps(dict(coarse=coarse, fine=fine,
                          nonlinear_point=result.x.tolist(),
                          nonlinear_value=float(result.fun))))


if __name__ == '__main__':
    main()
