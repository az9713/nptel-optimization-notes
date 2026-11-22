"""Small branch-and-bound with enumeration and independent MILP checks."""
from itertools import product
import json
import math

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp


def branch_and_bound(A, b, c, integer_indices, tolerance=1e-8, limit=100):
    """Maximize c @ x, nonnegative x; raise if search is unfinished."""
    A, b, c = (np.asarray(v, float) for v in (A, b, c))
    n = len(c)
    if A.ndim != 2 or A.shape != (len(b), n):
        raise ValueError("Incompatible arrays")
    if not all(np.isfinite(a).all() for a in (A, b, c)):
        raise ValueError("Coefficients must be finite")
    integer_indices = tuple(integer_indices)
    if any(j < 0 or j >= n for j in integer_indices):
        raise ValueError("Invalid integer variable index")
    stack = [[(0, None) for _ in range(n)]]
    incumbent, value, trace = None, -math.inf, []
    while stack:
        if len(trace) >= limit:
            raise RuntimeError("Node limit reached; optimality unproved")
        bounds = stack.pop()
        lp = linprog(-c, A_ub=A, b_ub=b, bounds=bounds, method="highs")
        row = {"bounds": bounds, "status": int(lp.status)}
        trace.append(row)
        if lp.status == 2:
            row["decision"] = "infeasible"
            continue
        if not lp.success:
            raise RuntimeError(f"LP status {lp.status}: {lp.message}")
        upper = float(-lp.fun)
        row["upper"] = upper
        if upper <= value + tolerance:
            row["decision"] = "bound"
            continue
        fractional = [j for j in integer_indices
                      if abs(lp.x[j] - round(lp.x[j])) > tolerance]
        if not fractional:
            candidate = lp.x.copy()
            candidate[list(integer_indices)] = np.round(
                candidate[list(integer_indices)])
            if np.any(A @ candidate > b + tolerance):
                raise RuntimeError("Rounded incumbent violates original rows")
            incumbent, value = candidate, float(c @ candidate)
            row["decision"] = "incumbent"
            continue
        j = fractional[0]
        lower, upper_bound = bounds[j]
        floor = math.floor(lp.x[j])
        left, right = bounds.copy(), bounds.copy()
        left[j] = (lower, min(floor, upper_bound)
                   if upper_bound is not None else floor)
        right[j] = (max(lower, floor + 1), upper_bound)
        stack.extend([left, right])
        row.update(decision="branch", variable=j)
    return incumbent, value, trace


def main():
    A, b, c = np.array([[6, 4], [1, 2]]), np.array([24, 6]), [5, 4]
    answer, value, trace = branch_and_bound(A, b, c, [0, 1])
    feasible = [np.array(x) for x in product(range(5), range(4))
                if np.all(A @ x <= b)]
    exact = max(feasible, key=lambda x: np.dot(c, x))
    assert np.array_equal(answer, [4, 0]) and value == 20
    assert np.array_equal(exact, answer)
    reference = milp(-np.array(c), integrality=[1, 1],
                     bounds=Bounds([0, 0], [np.inf, np.inf]),
                     constraints=LinearConstraint(A, [-np.inf] * 2, b))
    assert reference.success and np.isclose(-reference.fun, 20)
    relaxation = linprog(-np.array(c), A_ub=A, b_ub=b, method="highs")
    assert np.allclose(relaxation.x, [3, 1.5])
    assert np.isclose(-relaxation.fun, 21)
    assert all(6 * x[0] + 5 * x[1] <= 25 for x in feasible)
    assert 6 * relaxation.x[0] + 5 * relaxation.x[1] > 25
    assert all(sum(x) <= 4 for x in feasible)
    mixed_A, mixed_b = np.array([[3, 2], [0, 1]]), np.array([5, 2])
    mixed = milp([-1, -1], integrality=[1, 0],
                 constraints=LinearConstraint(mixed_A, [-np.inf] * 2, mixed_b))
    assert mixed.success and np.isclose(-mixed.fun, 2)
    assert len(trace) == 5
    print(json.dumps({"integer_optimum": answer.tolist(), "profit": value,
                      "lp_bound": 21, "nodes": trace,
                      "enumerated_feasible_points": len(feasible),
                      "mixed_optimum": float(-mixed.fun)}))


if __name__ == "__main__":
    main()
