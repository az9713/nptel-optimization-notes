"""Transportation cycle pivots and assignment certificates."""
from itertools import permutations
import json

import numpy as np
from scipy.optimize import linear_sum_assignment, linprog


def potentials(cost, basis):
    """Solve tree-edge equations u_i + v_j = cost_ij, fixing u_0 = 0."""
    cost = np.asarray(cost, float)
    m, n = cost.shape
    if not np.isfinite(cost).all() or len(basis) != m + n - 1:
        raise ValueError("Finite costs and a spanning-tree basis required")
    matrix, rhs = [], []
    for i, j in basis:
        row = np.zeros(m + n)
        row[i] = row[m + j] = 1
        matrix.append(row)
        rhs.append(cost[i, j])
    row = np.zeros(m + n)
    row[0] = 1
    matrix.append(row)
    rhs.append(0)
    answer = np.linalg.solve(matrix, rhs)
    return answer[:m], answer[m:]


def main():
    C = np.array([[2, 5, 4], [3, 1, 6]], float)
    supply, demand = np.array([4, 5]), np.array([3, 2, 4])
    first = np.array([[3, 1, 0], [0, 1, 4]], float)
    second = first + np.array([[0, -1, 1], [0, 1, -1]])
    final = second + 3 * np.array([[-1, 0, 1], [1, 0, -1]])
    costs = []
    for table in [first, second, final]:
        assert np.all(table >= 0)
        assert np.array_equal(table.sum(axis=1), supply)
        assert np.array_equal(table.sum(axis=0), demand)
        costs.append(float(np.sum(C * table)))
    assert costs == [36, 30, 27]
    u, v = potentials(C, [(0, 0), (0, 2), (1, 0), (1, 1)])
    assert np.allclose(u, [0, 1]) and np.allclose(v, [2, 0, 4])
    assert np.all(C - u[:, None] - v >= -1e-10)
    assert np.isclose(supply @ u + demand @ v, 27)
    rows = []
    for i in range(2):
        row = np.zeros((2, 3))
        row[i, :] = 1
        rows.append(row.ravel())
    for j in range(3):
        row = np.zeros((2, 3))
        row[:, j] = 1
        rows.append(row.ravel())
    reference = linprog(C.ravel(), A_eq=rows,
                        b_eq=np.concatenate((supply, demand)), method="highs")
    assert reference.success and np.isclose(reference.fun, 27)
    assignment = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]], float)
    reduced = assignment - np.array([1, 0, 2])[:, None] - [1, 0, 0]
    assert np.array_equal(reduced, [[2, 0, 2], [1, 0, 5], [0, 0, 0]])
    assignment_u, assignment_v = np.array([2, 1, 2]), np.array([1, -1, 0])
    final_reduced = assignment - assignment_u[:, None] - assignment_v
    assert np.array_equal(final_reduced, [[1, 0, 1], [0, 0, 4], [0, 1, 0]])
    row, column = linear_sum_assignment(assignment)
    optimum = float(assignment[row, column].sum())
    enumerated = min(sum(assignment[i, p[i]] for i in range(3))
                     for p in permutations(range(3)))
    assert optimum == enumerated == 5
    assert np.allclose(assignment_u.sum() + assignment_v.sum(), optimum)
    print(json.dumps({"shipping_costs": costs, "shipping_optimum": final.tolist(),
                      "potentials": {"u": u.tolist(), "v": v.tolist()},
                      "assignment_columns_zero_based": column.tolist(),
                      "assignment_cost": optimum}))


if __name__ == "__main__":
    main()
