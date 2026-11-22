"""Shortest paths, subtours, and a metric TSP approximation."""
from heapq import heappop, heappush
from itertools import permutations
from math import hypot, inf, isclose, isfinite


def dijkstra(graph, source):
    """Nonnegative finite weights; return distances and one predecessor tree."""
    if source not in graph:
        raise ValueError("source is absent")
    if any(v not in graph or not isfinite(w) or w < 0
           for neighbors in graph.values() for v, w in neighbors):
        raise ValueError("known vertices and finite nonnegative weights required")
    distances = dict.fromkeys(graph, inf)
    previous = dict.fromkeys(graph)
    distances[source] = 0
    queue = [(0, source)]
    while queue:
        distance, u = heappop(queue)
        if distance != distances[u]:
            continue
        for v, weight in graph[u]:
            candidate = distance + weight
            if candidate < distances[v]:
                distances[v] = candidate
                previous[v] = u
                heappush(queue, (candidate, v))
    return distances, previous


def brute_tour(cost):
    """Fix start at 0 and enumerate tours; intended only for tiny instances."""
    n = len(cost)
    return min((sum(cost[u][v] for u, v in zip(route, route[1:])), route)
               for tail in permutations(range(1, n))
               for route in [(0,) + tail + (0,)])


def tree_tour(points):
    """Prim MST plus preorder shortcut tour for a complete Euclidean graph."""
    n = len(points)
    cost = [[hypot(a[0] - b[0], a[1] - b[1]) for b in points] for a in points]
    tree = [[] for _ in points]
    reached = {0}
    tree_cost = 0
    while len(reached) < n:
        weight, u, v = min((cost[u][v], u, v) for u in reached
                           for v in range(n) if v not in reached)
        tree[u].append(v)
        tree[v].append(u)
        tree_cost += weight
        reached.add(v)
    order = []

    def visit(u, parent):
        order.append(u)
        for v in sorted(tree[u]):
            if v != parent:
                visit(v, u)

    visit(0, None)
    route = order + [0]
    length = sum(cost[u][v] for u, v in zip(route, route[1:]))
    return tree_cost, length, route, cost


if __name__ == "__main__":
    graph = {"s": [("a", 4), ("b", 1)], "b": [("a", 2), ("t", 7)],
             "a": [("t", 1)], "t": [], "z": []}
    distances, previous = dijkstra(graph, "s")
    assert distances == {"s": 0, "b": 1, "a": 3, "t": 4, "z": inf}
    assert previous["t"] == "a" and previous["a"] == "b"
    try:
        dijkstra({0: [(1, -1)], 1: []}, 0)
        raise AssertionError("negative edge was accepted")
    except ValueError:
        pass
    cost = [[inf, 1, 9, 9], [1, inf, 9, 9],
            [9, 9, inf, 1], [9, 9, 1, inf]]
    assignment = min(sum(cost[i][p[i]] for i in range(4))
                     for p in permutations(range(4)))
    optimum, route = brute_tour(cost)
    assert assignment == 4 and optimum == 20
    mst, approximate, order, matrix = tree_tour(
        [(0, 0), (2, 0), (2, 1), (0, 1), (1, 3)])
    exact, exact_order = brute_tour(matrix)
    assert mst <= exact + 1e-12
    assert exact <= approximate + 1e-12
    assert approximate <= 2 * mst + 1e-12
    assert len(set(order[:-1])) == 5 and order[0] == order[-1]
    print("shortest=4; assignment=4; TSP=20")
    print("metric MST=%.9f; preorder=%.9f; optimum=%.9f" %
          (mst, approximate, exact))
