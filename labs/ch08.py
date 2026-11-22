"""Derivative diagnostics checked by finite differences and exact examples."""
import numpy as np


def loss(z):
    u, v = np.asarray(z, float)
    return (u + v - 1) ** 2 + 2 * (u - v) ** 2


def gradient(z):
    u, v = np.asarray(z, float)
    return np.array([6 * u - 2 * v - 2, 6 * v - 2 * u - 2])


def central_gradient(function, point, step=1e-5):
    point = np.asarray(point, float)
    if point.ndim != 1 or not np.isfinite(point).all():
        raise ValueError("a finite one-dimensional parameter array is required")
    if not np.isfinite(step) or step <= 0:
        raise ValueError("step must be finite and positive")
    directions = np.eye(len(point)) * step
    return np.array([(function(point + d) - function(point - d)) / (2 * step)
                     for d in directions])


if __name__ == "__main__":
    hessian = np.array([[6, -2], [-2, 6]], float)
    optimum = np.linalg.solve(hessian, [2, 2])
    assert np.allclose(optimum, [0.5, 0.5])
    assert loss(optimum) == 0
    assert np.allclose(np.linalg.eigvalsh(hessian), [4, 8])
    for point in ([0, 0], [2, -1], [0.3, 0.8]):
        assert np.allclose(central_gradient(loss, point), gradient(point))
        direction = np.array([0.2, -0.1])
        difference = loss(np.array(point) + direction) - loss(point)
        taylor = gradient(point) @ direction + direction @ hessian @ direction / 2
        assert np.isclose(difference, taylor)
    stationary = [-1, 0, 1]
    assert [(x * x - 1) ** 2 for x in stationary] == [0, 1, 0]
    assert [12 * x * x - 4 for x in stationary] == [8, -4, 8]
    bad = np.diag([0.0, -1.0])
    assert bad[0, 0] == 0 and np.linalg.det(bad) == 0
    assert np.linalg.eigvalsh(bad).min() == -1
    # Identical zero Hessians at the origin, three distinct local behaviors.
    epsilon = 0.01
    assert epsilon ** 4 > 0
    assert -epsilon ** 4 < 0
    assert epsilon ** 4 - 0 ** 4 > 0 and 0 ** 4 - epsilon ** 4 < 0
    print("calibration optimum=(0.5,0.5), loss=0, Hessian eigenvalues=(4,8)")
