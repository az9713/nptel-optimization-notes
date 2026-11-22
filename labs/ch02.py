"""Small revised primal simplex; explicit two-phase teaching construction."""
import json

import numpy as np
from scipy.optimize import linprog


def simplex(M, b, c, basis, tolerance=1e-10, limit=100):
    """Maximize c @ z from a feasible basis; Bland ties, no file effects."""
    M, b, c = (np.asarray(value, float) for value in (M, b, c))
    m, n = M.shape
    basis = list(basis)
    if b.shape != (m,) or c.shape != (n,) or len(basis) != m:
        raise ValueError("Incompatible shapes or basis length")
    if len(set(basis)) != m or any(j < 0 or j >= n for j in basis):
        raise ValueError("Invalid basis indices")
    if not all(np.isfinite(a).all() for a in (M, b, c)):
        raise ValueError("Coefficients must be finite")
    trace = []
    for _ in range(limit):
        B = M[:, basis]
        beta = np.linalg.solve(B, b)
        if beta.min() < -tolerance:
            raise ValueError("Initial or updated basis is not primal feasible")
        y = np.linalg.solve(B.T, c[basis])
        reduced = c - M.T @ y
        z = np.zeros(n)
        z[basis] = beta
        trace.append({"basis": basis.copy(), "objective": float(c @ z)})
        eligible = [j for j in range(n)
                    if j not in basis and reduced[j] > tolerance]
        if not eligible:
            return {"status": "optimal", "z": z, "basis": basis,
                    "trace": trace, "reduced": reduced}
        entering = min(eligible)
        direction = np.linalg.solve(B, M[:, entering])
        rows = np.flatnonzero(direction > tolerance)
        if not len(rows):
            ray = np.zeros(n)
            ray[entering], ray[basis] = 1, -direction
            return {"status": "unbounded", "z": z, "ray": ray,
                    "basis": basis, "trace": trace}
        ratios = beta[rows] / direction[rows]
        tied = rows[np.isclose(ratios, ratios.min(), atol=tolerance, rtol=0)]
        leaving = min(tied, key=lambda row: basis[row])
        basis[leaving] = entering
    raise RuntimeError("Iteration limit reached")


def main():
    M = np.array([[1, 1, 1, 0], [2, 1, 0, 1]], float)
    b, c = np.array([4, 5]), np.array([3, 2, 0, 0])
    workshop = simplex(M, b, c, [2, 3])
    assert workshop["status"] == "optimal"
    assert np.allclose(workshop["z"], [1, 3, 0, 0])
    assert np.allclose([t["objective"] for t in workshop["trace"]],
                       [0, 7.5, 9])
    reference = linprog(-c[:2], A_ub=M[:, :2], b_ub=b, method="highs")
    assert reference.success and np.isclose(-reference.fun, 9)
    auxiliary = np.array([[1, 1, -1, 0, 1, 0],
                          [1, 3, 0, -1, 0, 1]], float)
    phase1 = simplex(auxiliary, [2, 3], [0, 0, 0, 0, -1, -1], [4, 5])
    assert phase1["status"] == "optimal"
    assert np.allclose(phase1["z"][4:], 0)
    assert all(j < 4 for j in phase1["basis"])
    phase2 = simplex(auxiliary[:, :4], [2, 3], [-1, -2, 0, 0],
                     phase1["basis"])
    assert np.allclose(phase2["z"][:2], [1.5, 0.5])
    assert np.isclose(np.dot([1, 2], phase2["z"][:2]), 2.5)
    unbounded = simplex([[1, -1, 1]], [1], [1, 2, 0], [2])
    assert unbounded["status"] == "unbounded"
    assert np.allclose(np.array([[1, -1, 1]]) @ unbounded["ray"], 0)
    assert np.dot([1, 2, 0], unbounded["ray"]) > 0
    unique = simplex([[1, 1, 1, 0], [0, 1, 0, 1]], [1, 0],
                     [1, 1, 0, 0], [0, 3])
    assert unique["status"] == "optimal"
    assert np.isclose(unique["reduced"][1], 0)
    assert np.allclose(unique["z"], [1, 0, 0, 0])
    print(json.dumps({"workshop_trace": workshop["trace"],
                      "two_phase_cost": 2.5,
                      "unbounded_ray": unbounded["ray"].tolist(),
                      "zero_reduced_cost_unique": True}))


if __name__ == "__main__":
    main()
