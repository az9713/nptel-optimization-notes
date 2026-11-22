"""Interpolation and descent: deterministic teaching checks, no I/O effects."""
import json

import numpy as np
from scipy.optimize import minimize, minimize_scalar


def quadratic_vertex(points, values):
    points = np.asarray(points, dtype=float)
    values = np.asarray(values, dtype=float)
    if points.shape != (3,) or values.shape != (3,):
        raise ValueError('Three points and three values are required')
    if not np.isfinite(points).all() or not np.isfinite(values).all():
        raise ValueError('Inputs must be finite')
    if not points[0] < points[1] < points[2]:
        raise ValueError('Points must be distinct and increasing')
    origin = points[1]
    a, b, _ = np.polyfit(points - origin, values, 2)
    if a <= 0:
        raise ValueError('The interpolating parabola has no strict minimum')
    return float(origin - b / (2 * a))


def objective(x):
    a, b = x
    return 2 * a * a + 2 * a * b + b * b + a - b


def main():
    vertex = quadratic_vertex([0, 1, 3], [5, 2, 2])
    assert np.isclose(vertex, 2)
    hessian = np.array([[4., 2.], [2., 2.]])
    linear = np.array([1., -1.])
    x = np.zeros(2)
    trace = [x.copy()]
    previous = objective(x)
    for _ in range(100):
        gradient = hessian @ x + linear
        if np.linalg.norm(gradient) < 1e-10:
            break
        alpha = (gradient @ gradient) / (gradient @ hessian @ gradient)
        x = x - alpha * gradient
        assert objective(x) <= previous + 1e-12
        previous = objective(x)
        trace.append(x.copy())
    assert np.allclose(trace[1], [-1, 1])
    assert np.allclose(trace[2], [-.8, 1.2])
    assert np.allclose(x, [-1, 1.5], atol=1e-8)
    assert np.isclose(objective(x), -1.25)
    simplex = np.array([[4., 4.], [5., 4.], [4., 5.]])
    centroid = (simplex[0] + simplex[2]) / 2
    reflection = 2 * centroid - simplex[1]
    expansion = centroid + 2 * (reflection - centroid)
    assert np.allclose([objective(z) for z in simplex], [80, 107, 96])
    assert np.isclose(objective(reflection), 71)
    assert np.isclose(objective(expansion), 56.75)
    result = minimize(objective, [4., 4.], method='Nelder-Mead',
                      options={'xatol': 1e-10, 'fatol': 1e-12})
    assert result.success and np.allclose(result.x, [-1, 1.5], atol=1e-7)
    scalar = minimize_scalar(lambda z: (z - 2) ** 2 + 1,
                             bounds=(0, 3), method='bounded')
    assert scalar.success and np.isclose(scalar.x, vertex)
    print(json.dumps(dict(vertex=vertex, optimum=x.tolist(),
                          value=objective(x), first_two_steps=[
                              z.tolist() for z in trace[1:3]],
                          reflection_value=objective(reflection),
                          expansion_value=objective(expansion))))


if __name__ == '__main__':
    main()
