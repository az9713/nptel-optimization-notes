"""Two-dimensional LP vertices checked against an independent LP solver."""
from itertools import combinations
import json

import numpy as np
from scipy.optimize import linprog


def vertices_2d(A, b, tolerance=1e-10):
    """Return feasible pairwise boundary intersections; no boundedness claim."""
    A, b = np.asarray(A, float), np.asarray(b, float)
    if A.ndim != 2 or A.shape[1] != 2 or b.shape != (len(A),):
        raise ValueError("Expected A of shape (m, 2) and b of shape (m,)")
    if not np.isfinite(A).all() or not np.isfinite(b).all():
        raise ValueError("Coefficients must be finite")
    points = []
    for indices in combinations(range(len(A)), 2):
        rows = list(indices)
        if abs(np.linalg.det(A[rows])) <= tolerance:
            continue
        point = np.linalg.solve(A[rows], b[rows])
        if np.all(A @ point <= b + tolerance):
            if not any(np.allclose(point, old) for old in points):
                points.append(point)
    return np.array(points).reshape(-1, 2)


def main():
    A = np.array([[1, 1], [2, 1], [-1, 0], [0, -1]], float)
    b = np.array([4, 5, 0, 0], float)
    c = np.array([3, 2], float)
    vertices = vertices_2d(A, b)
    profits = vertices @ c
    best = vertices[np.argmax(profits)]
    reference = linprog(-c, A_ub=A[:2], b_ub=b[:2], method="highs")
    assert len(vertices) == 4
    assert np.allclose(best, [1, 3])
    assert np.isclose(profits.max(), 9)
    assert reference.success and np.allclose(reference.x, best)
    assert np.isclose(-reference.fun, 9)
    edge_values = vertices @ np.ones(2)
    assert np.count_nonzero(np.isclose(edge_values, 4)) == 2
    infeasible = linprog([1], A_ub=[[1]], b_ub=[-1], method="highs")
    assert infeasible.status == 2
    unbounded = linprog([-1], method="highs")
    assert unbounded.status == 3
    print(json.dumps({"vertices": vertices.tolist(), "optimum": best.tolist(),
                      "profit": 9, "optimal_edge_vertices": 2,
                      "infeasible_status": infeasible.status,
                      "unbounded_status": unbounded.status}))


if __name__ == "__main__":
    main()
