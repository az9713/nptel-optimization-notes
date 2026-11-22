"""Dynamic programming and independent exhaustive checks."""
import itertools
import json

import numpy as np


def knapsack(weights, values, capacity):
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError('Capacity must be a nonnegative integer')
    if len(weights) != len(values) or not weights:
        raise ValueError('Nonempty matching item arrays required')
    if any(not isinstance(w, int) or w <= 0 for w in weights):
        raise ValueError('Weights must be positive integers')
    if not np.isfinite(values).all():
        raise ValueError('Values must be finite')
    count = len(weights)
    table = np.zeros((count + 1, capacity + 1))
    policy = np.zeros((count, capacity + 1), dtype=int)
    for i in range(count - 1, -1, -1):
        for remaining in range(capacity + 1):
            candidates = [q * values[i] + table[i + 1, remaining - q * weights[i]]
                          for q in range(remaining // weights[i] + 1)]
            q = int(np.argmax(candidates))
            table[i, remaining] = candidates[q]
            policy[i, remaining] = q
    remaining, choices = capacity, []
    for i, w in enumerate(weights):
        q = int(policy[i, remaining])
        choices.append(q)
        remaining -= q * w
    return float(table[0, capacity]), choices, table


def main():
    value, choices, table = knapsack([3, 4, 6], [7, 8, 11], 10)
    brute = max((7 * a + 8 * b + 11 * c, [a, b, c])
                for a, b, c in itertools.product(range(4), range(3), range(2))
                if 3 * a + 4 * b + 6 * c <= 10)
    assert value == brute[0] == 22 and choices == [2, 1, 0]
    assert table[1, 10] == 19
    failures = [[.4, .2, .15], [.6, .4, .2], [.8, .5, .3]]
    allocations = [(np.prod([failures[i][q] for i, q in enumerate(qs)]), qs)
                   for qs in itertools.product(range(3), repeat=3)
                   if sum(qs) == 2]
    failure, allocation = min(allocations)
    assert np.isclose(failure, .06) and allocation == (1, 0, 1)
    assert np.isclose(np.prod([5 / 3] * 3), 125 / 27)
    assert sum(x * x for x in [5, 5, 5]) == 75
    # Two equal-length prefixes can have different admissible continuations.
    histories = [('start', 'A', 'C'), ('start', 'B', 'C')]
    assert histories[0][-1] == histories[1][-1]
    assert ('A' in histories[0]) != ('A' in histories[1])
    print(json.dumps(dict(knapsack_value=value, knapsack_choices=choices,
                          two_type_values=table[1].tolist(),
                          research_failure=float(failure),
                          research_allocation=allocation)))


if __name__ == '__main__':
    main()
