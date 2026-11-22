"""Critical-path analysis checked against independent path enumeration."""
from itertools import product
from math import erf, isclose, sqrt


EDGES = [
    (1, 2, 3, "A"), (1, 3, 2, "B"), (2, 4, 4, "C"),
    (3, 4, 6, "D"), (2, 5, 2, "E"), (4, 6, 2, "F"),
    (5, 6, 4, "G"),
]


def analyze(edges):
    """Return earliest/latest event times and activity total floats.

    Contract: integer nodes 1..n are topologically ordered; all durations
    finite and nonnegative; every node lies on a 1-to-n path.
    """
    from math import isfinite

    if not edges:
        raise ValueError("a nonempty DAG is required")
    nodes = sorted({v for u, v, _, _ in edges} | {u for u, _, _, _ in edges})
    if nodes != list(range(1, max(nodes) + 1)):
        raise ValueError("nodes must be 1..n")
    if any(u >= v or not isfinite(t) or t < 0 for u, v, t, _ in edges):
        raise ValueError("topological arcs and nonnegative durations required")
    earliest = {1: 0.0}
    for v in nodes[1:]:
        candidates = [earliest[u] + t for u, w, t, _ in edges if w == v
                      and u in earliest]
        if not candidates:
            raise ValueError("every node must be reachable from node 1")
        earliest[v] = max(candidates)
    latest = {nodes[-1]: earliest[nodes[-1]]}
    for u in reversed(nodes[:-1]):
        candidates = [latest[v] - t for w, v, t, _ in edges if w == u
                      and v in latest]
        if not candidates:
            raise ValueError("every node must reach the final node")
        latest[u] = min(candidates)
    floats = {name: latest[v] - earliest[u] - t for u, v, t, name in edges}
    return earliest, latest, floats


def paths(edges, node=1, labels=(), duration=0):
    """Enumerate all paths, independently of the forward/backward recurrence."""
    final = max(v for _, v, _, _ in edges)
    if node == final:
        return [(labels, duration)]
    result = []
    for u, v, t, name in edges:
        if u == node:
            result.extend(paths(edges, v, labels + (name,), duration + t))
    return result


if __name__ == "__main__":
    earliest, latest, floats = analyze(EDGES)
    assert earliest == {1: 0, 2: 3, 3: 2, 4: 8, 5: 5, 6: 10}
    assert latest == {6: 10, 5: 6, 4: 8, 3: 2, 2: 4, 1: 0}
    assert {k for k, v in floats.items() if isclose(v, 0)} == {"B", "D", "F"}
    assert max(t for _, t in paths(EDGES)) == earliest[6]
    tied = [(u, v, 3 if name == "E" else t, name) for u, v, t, name in EDGES]
    assert sum(t == 10 for _, t in paths(tied)) == 2
    assert analyze(tied)[0][6] == 10
    # Reduce B only: its former critical path becomes 9, so another path binds.
    crashed = [(u, v, t - (name == "B"), name) for u, v, t, name in EDGES]
    assert analyze(crashed)[0][6] == 9
    crashed_again = [(u, v, t - (name == "B"), name)
                     for u, v, t, name in crashed]
    assert analyze(crashed_again)[0][6] == 9
    variance = (2 / 6) ** 2 + (4 / 6) ** 2 + (2 / 6) ** 2
    probability = 0.5 * (1 + erf(1 / sqrt(2 * variance)))
    assert isclose(variance, 2 / 3)
    assert isclose(probability, 0.8896643190400766)
    # Two independent path times, each equally likely to be 9 or 11 days.
    outcomes = list(product((9, 11), repeat=2))
    assert sum(max(a, b) <= 10 for a, b in outcomes) / 4 == 0.25
    print("duration=10; critical=B,D,F; P(fixed path<=11)=%.9f" % probability)
