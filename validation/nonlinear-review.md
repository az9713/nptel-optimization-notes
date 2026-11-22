# Independent scientific review: chapters 11–16 and interactive lab

Reviewer: `network_classical`, independent of the author of chapters 11–16 and the author of the interactive lab.

Disposition: accepted after the three bounded repairs below. No material scientific findings remain in the reviewed files. Exact accepted bytes are identified in `nonlinear-review.json`; any subsequent edit invalidates acceptance for that file until checked again.

## Coverage and evidence

Read all six chapter manuscripts, their JSON metadata, and their Python labs end to end. Examined the derivations, teaching cases, limitations, and all six worked solutions per chapter against the explanatory depth of both older Stanford exemplars used for this project. Read `numerical-lab.md` and `assets/lab.js` completely. This is a scientific and algorithmic review, not a browser accessibility or visual-layout acceptance.

Read all six author source-reading ledgers and checked that every lecture 29–40 digest and caption-coverage endpoint agrees with `source-manifest.json`. These ledgers document the author's full sequential caption reading. Independently spot-checked the actual caption segments for lecture 29 at 1025–1190 seconds (two values and one derivative), lecture 32 at 2321–2490 seconds (direction subproblem and feasible step length), and lecture 40 at 1318–1470 seconds (AHP column normalization versus eigenvector) and 3180–3455 seconds (TOPSIS relative closeness and contradictory closing ranking). The chapter repairs and distinctions faithfully address these sampled passages. The reviewer did not independently reread all captions, listen to the audio, or inspect all boards. Full author caption coverage must not be described as a second exhaustive audiovisual review.

Consulted primary references for important external guarantees: [Boyd and Vandenberghe, Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf), especially convexity, KKT sufficiency and sensitivity; [Boyd et al., a GP tutorial](https://web.stanford.edu/~boyd/papers/pdf/gp_tutorial.pdf), especially standard form and logarithmic transformation; [MIT 6.231 lecture 2](https://ocw.mit.edu/courses/6-231-dynamic-programming-and-stochastic-control-fall-2015/2beec55b0de261096962e514febe3b5c_MIT6_231F15_Lec2.pdf), for the dynamic-programming principle and sufficient state; and the [restricted Nelder–Mead convergence paper](https://arxiv.org/abs/1104.0350), for the need to distinguish algorithm variants and assumptions. Also inspected official [SciPy scalar-minimization documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize_scalar.html) and [Gurobi constraint documentation](https://docs.gurobi.com/projects/optimizer/en/current/concepts/modeling/constraints.html). Publisher full text for the cited AHP and TOPSIS papers returned access errors; no full-paper verification is claimed. Their numerical procedures were checked directly from the displayed equations and independently recomputed.

## Repairs made during review

1. Chapter 11: supplied the missing derivation of the strong-convexity gradient-to-objective-gap bound by completing the square. This makes its curvature assumption and auxiliary minimization explicit.
2. Chapter 12: added the equality-Jacobian constraint to the simplified feasible-direction LP, defined the row convention, and stated that nonlinear equalities are preserved only to first order and still need restoration.
3. Chapter 16: rejected AHP matrices of order below two, where the displayed consistency-index denominator is undefined, added the singleton rejection regression to the lab, and updated the manuscript's lab contract.

## Mathematical checks

- Chapter 11: recovered the quadratic optimum, exact line-search steps, interpolation coefficients, and reflection/expansion arithmetic. The stopping diagnostics distinguish stationarity, objective guarantees and algorithmic success flags.
- Chapter 12: recomputed the finite-parameter exterior-penalty, inverse-barrier and log-barrier minimizers and the cutting-plane iterates. Verified the tangent-versus-feasible-step distinction and the conditions on the barrier gap.
- Chapter 13: checked the SOS2 adjacency requirement, interpolation error bound, coarse separable-program solution and actual nonlinear resource usage. The finite-cell enumeration certifies the stated discretized model rather than the original nonlinear problem without an error argument.
- Chapter 14: checked exponent balance, the log-sum-exp covariance Hessian, the AM–GM lower bound, and the constrained example's primal and dual recovery. The restrictions on positive variables, coefficient signs and reversed posynomial inequalities are explicit.
- Chapter 15: recomputed the capacity-10 knapsack value 22, the continuous allocation solutions, and all six research-team allocations. The best independent-failure product is 0.060. State sufficiency, exact filling versus unused capacity, and decision timing are distinguished.
- Chapter 16: checked unsupported Pareto points, epsilon-constraint recovery, criterion-space geometry and goal deviations. Independent JavaScript arithmetic recovered AHP weights approximately (0.507603, 0.113269, 0.379129), Perron root 3.163235 and consistency index 0.081617. TOPSIS closeness values were (0.475993, 0.564057, 0.524007) with equal weights and (0.185066, 0.743996, 0.814934) for the stated cost-heavy case. These agree with the chapter.

## Interactive lab acceptance

For the resource LP, independently checked the three value-function pieces: `3b` on 0≤b≤2, `2b+2` on 2≤b≤5, and 12 for b≥5. The selected shadow prices 3, 2 and 0 are valid, and the breakpoint intervals [2,3] at b=2 and [0,2] at b=5 are correct. At b=0 the full multiplier set is [3,infinity); displaying the representative 3 is valid and does not assert uniqueness. Checked primal-dual equality at b=0,1,2,3,5,7.

For the quadratic-conditioning panel, the Hessian is diag(1,kappa), step size is 1/kappa, the second component vanishes after one step, and the remaining component contracts by 1−1/kappa. The plotted relative loss divides by the initial loss (1+kappa)/2, consistent with the implementation. The kappa=1 finite termination and the log-plot floor are correctly distinguished.

## Execution boundary

This reviewer inspected all Python lab implementations and recomputed the central examples, but did not independently execute every Python lab after review edits. Native imports were slow under the shared machine's concurrent workload. The author reported chapter 12 and chapter 16 passing; chapter 13 already had a pending optimized rerun, so the reviewer did not start a duplicate. Final sequential execution or CI remains the root agent's release gate. Acceptance here covers the mathematics and inspected code; it does not replace that execution gate.
