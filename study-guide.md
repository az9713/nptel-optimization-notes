# Study guide

## Three questions to ask before solving

First identify the decision variables and their domains. A real-valued quantity can be divisible production or time; an integer or binary quantity represents a discrete choice. Replacing one domain by another changes the problem even when every coefficient is unchanged.

Next identify what makes a candidate feasible. Linear resource limits, flow conservation, precedence, smooth inequalities and a finite-state transition rule each support different algorithms. A shared word such as “allocation” does not imply a shared mathematical structure.

Finally ask what certificate the method returns. A primal–dual equality can certify global LP optimality. A vanishing gradient generally certifies only stationarity. A Bellman recursion certifies optimality only for a correctly specified state and complete admissible action set. A weighted score encodes a preference model rather than discovering an objective social ranking.

## Reading paths

| Goal | Read | Prerequisites |
|---|---|---|
| Formulate and certify resource allocation | Chapters 1–3 | Linear algebra; inequalities |
| Model indivisible choices and routing | Chapters 4–7 | LP bounds; graph terminology |
| Understand local and constrained smooth methods | Chapters 8–12 | Multivariable calculus; Taylor expansions |
| Exploit structured nonlinear models | Chapters 13–14 | Convexity; logarithms; LP approximation |
| Make sequential and multicriteria decisions | Chapters 15–16 | State transitions; probability; explicit preferences |

A useful first pass reads the opening model, one derivation, the worked example and the limitation in each chapter. A second pass reproduces the laboratory and solves the exercises without opening the solutions. For research use, inspect the assumptions of a theorem before transferring its conclusion to a new model.

## Method map

| Structure | Method family | What needs checking |
|---|---|---|
| Linear objective and polyhedral constraints | Simplex or LP solver | Feasibility, reduced costs, tolerances, dual certificate |
| Integer restrictions | Branch and bound; valid cuts | Bound direction, incumbent feasibility, termination gap |
| Supplies, demands and separable shipping costs | Transportation/network methods | Balance, conservation, degeneracy, integrality conditions |
| Project precedence | Longest path in a DAG; CPM | Valid DAG, all critical paths, resource constraints omitted |
| Nonnegative shortest-path costs | Dijkstra | Nonnegative arcs; negative cycles require different reasoning |
| One-dimensional unimodal objective | Region elimination | Bracket validity; strictness/tie conventions; evaluation cost |
| Smooth multivariate objective | Gradient/Newton/direct search | Descent, line search, conditioning, local versus global claims |
| Smooth constraints | KKT, penalties, barriers | Constraint qualification, convexity, penalty limit, residuals |
| Positive-variable posynomials | Log-transformed geometric program | Positive coefficients; admissible equality/inequality forms |
| Finite-horizon state/action model | Dynamic programming | Sufficient state; full transition model; boundary conditions |
| Several conflicting objectives | Pareto analysis; preference model | Scaling, unsupported efficient points, stakeholder weights |

## A bridge to contemporary AI

Optimization in AI combines structures taught separately here. A model-training loss may be nonconvex; a serving scheduler may be a mixed-integer program; a decoding or tool-use policy may be sequential; and a latency–accuracy tradeoff is multiobjective. Choose a method from the mathematical structure, then ask what guarantee survives the approximation.

An instructive solo project is a small inference-workload allocator. Begin with the LP from chapter 1 and use dual prices to quantify scarce capacity. Add binary deployment choices and compare the integer optimum with the LP bound. Add a daily workload state and solve a finite-horizon dynamic program. Finally expose cost, delay and reliability separately before imposing preference weights. This progression makes relaxation error, state misspecification and value judgments independently measurable. It is a proposed exercise, not an evaluated production system.

## Reproduce the computations

Install the packages in `requirements.txt`, then run `python tools/check.py`. Each laboratory is also runnable as `python labs/chNN.py`. The checker executes labs in fresh processes, checks the coverage map and local links, and records results under `validation/`. Browser validation checks actual MathJax output and reader behavior at desktop and phone widths. These checks support numerical and presentation claims; they do not replace mathematical review.
