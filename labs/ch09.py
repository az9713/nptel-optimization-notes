"""KKT equations verified against all active sets of a small convex QP."""
from itertools import combinations

import numpy as np


def active_set_solutions(center, matrix, bounds, tolerance=1e-9):
    """Solve min ||x-center||^2 subject to matrix @ x <= bounds.

    Enumerates independent active sets up to parameter dimension; finite,
    tiny teaching instances only. Returns feasible KKT candidate triples.
    """
    center = np.asarray(center, float)
    matrix = np.asarray(matrix, float)
    bounds = np.asarray(bounds, float)
    n = len(center)
    if (center.ndim != 1 or matrix.ndim != 2 or matrix.shape[1] != n
            or bounds.shape != (len(matrix),)
            or not all(np.isfinite(a).all() for a in (center, matrix, bounds))):
        raise ValueError("finite arrays with compatible dimensions required")
    candidates = []
    for size in range(min(n, len(matrix)) + 1):
        for active in combinations(range(len(matrix)), size):
            selected = matrix[list(active)]
            kkt = np.block([[2 * np.eye(n), selected.T],
                            [selected, np.zeros((size, size))]])
            rhs = np.r_[2 * center, bounds[list(active)]]
            try:
                answer = np.linalg.solve(kkt, rhs)
            except np.linalg.LinAlgError:
                continue
            x, values = answer[:n], answer[n:]
            if np.all(matrix @ x <= bounds + tolerance) and np.all(values >= -tolerance):
                multipliers = np.zeros(len(matrix))
                multipliers[list(active)] = values
                candidates.append((x, multipliers, active))
    return candidates


if __name__ == "__main__":
    matrix = np.array([[1, 1], [-2, 1], [-1, 0], [0, -1]], float)
    bounds = np.array([3, 2, 0, 0], float)
    candidates = active_set_solutions([2, 3], matrix, bounds)
    assert candidates
    for x, multipliers, active in candidates:
        assert np.allclose(x, [1, 2])
        assert np.allclose(multipliers, [2, 0, 0, 0])
        assert np.allclose(2 * (x - [2, 3]) + matrix.T @ multipliers, 0)
        assert np.allclose(multipliers * (matrix @ x - bounds), 0)
        assert np.isclose(np.sum((x - [2, 3]) ** 2), 2)
    a = np.array([[1.0, 1.0, 2.0]])
    bordered = np.block([[2 * np.eye(3), a.T], [a, np.zeros((1, 1))]])
    answer = np.linalg.solve(bordered, [0, 0, 0, 12])
    assert np.allclose(answer, [2, 2, 4, -4])
    eigenvalues = np.linalg.eigvalsh(bordered)
    assert eigenvalues.min() < 0 < eigenvalues.max()
    epsilon = 1e-5
    value = lambda b: b * b / 6
    sensitivity = (value(12 + epsilon) - value(12 - epsilon)) / (2 * epsilon)
    assert np.isclose(sensitivity, 4)
    print("inequality optimum=(1,2), loss=2, lambda=(2,0,0,0)")
    print("equality optimum=(2,2,4), objective=24, multiplier=-4")
