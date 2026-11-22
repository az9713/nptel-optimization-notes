"""Dual certificates and sensitivity checked with independent LP solves."""
import json

import numpy as np
from scipy.optimize import linprog


def dual_simplex(M, b, c, basis, tolerance=1e-10, limit=100):
    """Maximization dictionary with nonpositive reduced costs; dense demo."""
    M, b, c = (np.asarray(v, float) for v in (M, b, c))
    m, n = M.shape
    basis = list(basis)
    if b.shape != (m,) or c.shape != (n,) or len(set(basis)) != m:
        raise ValueError("Incompatible arrays or invalid basis")
    if not all(np.isfinite(a).all() for a in (M, b, c)):
        raise ValueError("Use finite arrays")
    trace = []
    for _ in range(limit):
        B = M[:, basis]
        beta = np.linalg.solve(B, b)
        y = np.linalg.solve(B.T, c[basis])
        reduced = c - M.T @ y
        if reduced.max() > tolerance:
            raise ValueError("Basis is not dual feasible")
        z = np.zeros(n)
        z[basis] = beta
        trace.append({"basis": basis.copy(), "basic": beta.tolist()})
        if beta.min() >= -tolerance:
            return {"status": "optimal", "z": z, "trace": trace}
        row = int(np.argmin(beta))
        transformed = np.linalg.solve(B, M)
        candidates = [j for j in range(n) if j not in basis
                      and transformed[row, j] < -tolerance]
        if not candidates:
            return {"status": "infeasible", "trace": trace}
        entering = min(candidates,
                       key=lambda j: (reduced[j] / transformed[row, j], j))
        basis[row] = entering
    raise RuntimeError("Iteration limit reached")


def main():
    A, b, c = np.array([[1, 1], [2, 1]]), np.array([4, 5]), [3, 2]
    primal = linprog(-np.array(c), A_ub=A, b_ub=b, method="highs")
    dual = linprog(b, A_ub=-A.T, b_ub=-np.array(c), method="highs")
    assert primal.success and dual.success
    assert np.allclose(primal.x, [1, 3]) and np.allclose(dual.x, [1, 1])
    assert np.isclose(-primal.fun, dual.fun)
    assert np.allclose(dual.x * (b - A @ primal.x), 0)
    assert np.allclose(primal.x * (A.T @ dual.x - c), 0)
    values = []
    for delta in [-1.5, -1, 0, 0.5, 1, 2]:
        changed = linprog(-np.array(c), A_ub=A, b_ub=b + [delta, 0],
                          method="highs")
        assert changed.success
        expected = 9 + delta if delta <= 1 else 10
        assert np.isclose(-changed.fun, expected)
        values.append([delta, float(-changed.fun)])
    for eta in [-1, -0.5, 0, 0.5, 1]:
        changed = linprog([-3 - eta, -2], A_ub=A, b_ub=b, method="highs")
        assert changed.success and np.isclose(-changed.fun, 9 + eta)
    M = np.column_stack((A, np.eye(2)))
    repaired = dual_simplex(M, [6, 5], [3, 2, 0, 0], [0, 1])
    assert repaired["status"] == "optimal"
    assert np.allclose(repaired["z"], [0, 5, 1, 0])
    reference = linprog([-3, -2], A_ub=A, b_ub=[6, 5], method="highs-ds")
    assert reference.success and np.isclose(-reference.fun, 10)
    capped = linprog([-3, -2], A_ub=np.vstack((A, [0, 1])),
                     b_ub=[4, 5, 2], method="highs")
    assert np.allclose(capped.x, [1.5, 2]) and np.isclose(-capped.fun, 8.5)
    print(json.dumps({"primal": primal.x.tolist(), "dual": dual.x.tolist(),
                      "capacity_sweep": values, "dual_simplex": repaired,
                      "added_constraint_profit": 8.5},
                     default=lambda v: v.tolist()))


if __name__ == "__main__":
    main()
