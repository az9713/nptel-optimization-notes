"""Pareto screening, AHP consistency, and TOPSIS sensitivity."""
import json

import numpy as np


def pareto_min(points):
    points = np.asarray(points, float)
    if points.ndim != 2 or not np.isfinite(points).all():
        raise ValueError('Use a finite alternatives-by-objectives matrix')
    return [i for i, point in enumerate(points)
            if not any(np.all(other <= point) and np.any(other < point)
                       for other in points)]


def ahp(matrix):
    matrix = np.asarray(matrix, float)
    if (matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]
            or matrix.shape[0] < 2):
        raise ValueError('Use a square comparison matrix of order at least two')
    if not np.isfinite(matrix).all() or np.any(matrix <= 0):
        raise ValueError('Comparisons must be finite and positive')
    if not np.allclose(matrix * matrix.T, 1):
        raise ValueError('Comparisons must be reciprocal')
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    index = np.argmax(eigenvalues.real)
    weights = eigenvectors[:, index].real
    weights /= weights.sum()
    eigenvalue = float(eigenvalues[index].real)
    ci = (eigenvalue - len(matrix)) / (len(matrix) - 1)
    return weights, eigenvalue, ci


def topsis(matrix, weights, benefit):
    matrix = np.asarray(matrix, float)
    weights = np.asarray(weights, float)
    benefit = np.asarray(benefit, bool)
    if matrix.ndim != 2 or min(matrix.shape) == 0:
        raise ValueError('Use a nonempty decision matrix')
    if weights.shape != (matrix.shape[1],) or benefit.shape != weights.shape:
        raise ValueError('One weight and direction per criterion required')
    if not np.isfinite(matrix).all() or not np.isfinite(weights).all():
        raise ValueError('All values must be finite')
    if np.any(weights < 0) or not np.isclose(weights.sum(), 1):
        raise ValueError('Nonnegative weights must sum to one')
    norms = np.linalg.norm(matrix, axis=0)
    if np.any(norms == 0):
        raise ValueError('Remove zero-norm criteria')
    weighted = matrix / norms * weights
    ideal = np.where(benefit, weighted.max(0), weighted.min(0))
    anti = np.where(benefit, weighted.min(0), weighted.max(0))
    positive = np.linalg.norm(weighted - ideal, axis=1)
    negative = np.linalg.norm(weighted - anti, axis=1)
    if np.any(positive + negative == 0):
        raise ValueError('All effective criteria coincide; ranking undefined')
    return negative / (positive + negative)


def main():
    points = [[0., 2.], [1., 1.2], [2., 0.], [2., 2.]]
    assert pareto_min(points) == [0, 1, 2]
    for weight in np.linspace(.001, .999, 999):
        scores = np.asarray(points) @ [weight, 1 - weight]
        assert int(np.argmin(scores)) != 1
    consistent = np.array([[1., 2., 4.], [.5, 1., 2.], [.25, .5, 1.]])
    weights, eigenvalue, ci = ahp(consistent)
    assert np.allclose(weights, [4 / 7, 2 / 7, 1 / 7])
    assert np.isclose(eigenvalue, 3) and abs(ci) < 1e-12
    try:
        ahp([[1.]])
    except ValueError:
        pass
    else:
        raise AssertionError('Order-one consistency index must be rejected')
    inconsistent = np.array([[1., 3., 2.], [1 / 3, 1., 1 / 5],
                             [.5, 5., 1.]])
    priorities, largest, inconsistency = ahp(inconsistent)
    row_approx = (inconsistent / inconsistent.sum(axis=0)).mean(axis=1)
    matrix = [[17., 12.], [10., 8.], [8., 6.]]
    equal = topsis(matrix, [.5, .5], [False, True])
    cost_heavy = topsis(matrix, [.8, .2], [False, True])
    assert np.allclose(equal, topsis(np.asarray(matrix) * [1000., 1.],
                                    [.5, .5], [False, True]))
    assert np.argmax(equal) != np.argmax(cost_heavy)
    print(json.dumps(dict(ahp_weights=weights.tolist(),
                          inconsistent_priorities=priorities.tolist(),
                          row_average_approximation=row_approx.tolist(),
                          largest_eigenvalue=largest,
                          consistency_index=inconsistency,
                          topsis_equal_weights=equal.tolist(),
                          topsis_cost_heavy=cost_heavy.tolist())))


if __name__ == '__main__':
    main()
