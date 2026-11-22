# Independent scientific review: chapters 6–10

Reviewer: `linear_discrete`, independent of chapter author `network_classical`.
Standard: local `science-editor` skill and `EDITOR_DOMAIN.md`.

## Verdict

Accepted for scientific content within the evidence boundary below. The chapters develop the mechanisms rather than merely list algorithms. Definitions, hypotheses, worked examples, counterexamples, and all thirty exercise solutions were read and checked. No blocking mathematical or pedagogical defect remains. Acceptance binds the fifteen Markdown, metadata, and Python bodies hashed in `review-network.json`; it does not certify later edits or replace the final execution gate.

## Findings and repairs

The chapter 7 approximation citation originally pointed to an entire MIT course. Replaced it with the verified lecture 17 PDF, page 1, and identified its role as the general definition of an approximation ratio. The metric-tour guarantee remains supported by the chapter's own explicit proof. This was a citation-locator improvement, not a correction to the bound.

No further line-level or structural repair was required. In particular, the chapters preserve the distinction between a longest-path recurrence and resource-constrained scheduling; a PERT path approximation and the distribution of a maximum; tentative and settled shortest-path labels; a cycle cover and a connected tour; stationary and globally optimal points; necessary KKT conditions and convex sufficiency; and a parameter interval and objective accuracy.

## Mathematical and laboratory inspection

- Chapter 6: recomputed both network passes, critical path B–D–F of length 10, activity floats, path-switching crash example, and the two-path uncertainty counterexample. Checked the PERT mean and variance calculation and all six solutions.
- Chapter 7: checked Dijkstra's invariant, negative-edge counterexample, subtour constraints, Hamiltonian-cycle reduction, and the doubled-tree metric proof. Recomputed shortest distance 4, cycle-cover cost 4 versus connected-tour cost 20, and the five-point Euclidean construction. Checked all six solutions.
- Chapter 8: checked scalar higher-order tests, the local Hessian argument, principal-minor qualifications, the two-parameter Hessian and optimum, and convex local-to-global proof. Checked all six solutions, including semidefinite counterexamples.
- Chapter 9: checked the tangent-space derivation, reduced curvature with the Lagrangian Hessian, singular-constraint counterexample, multiplier signs, complete KKT conditions, convex certificate, and sensitivity sign. Recomputed equality optimum (2,2,4), value 24, and inequality optimum (1,2), value 2, multiplier 2. Checked all six solutions.
- Chapter 10: checked strict-unimodality elimination including ties, grid localization, dichotomous recurrence, interval-halving reuse, Fibonacci indexing and conservative terminal width, golden fixed point, and evaluation counts. Ten golden reductions require eleven values and give width 0.056914331 for initial width 7. Checked all six solutions.

All five Python labs were read in full against these models. The author reports that each passed with exit 0 and assertions satisfied; the exact reported outputs are recorded in the JSON receipt. This reviewer did not perform a duplicate post-review execution batch. Root's final sequential execution or CI remains required. Manuscript acceptance is not a claim that an unobserved run succeeded.

## Source and citation checks

Inspected all five metadata files and source ledgers. Their thirteen transcript digests and endpoints match the source manifest. Independently inspected twenty-six bounded caption passages, two for each lecture 16–28; the exact spans are recorded in the JSON receipt. They support the mapped topic sequence and timestamp anchors. This is selective independent source checking, not a full caption reread, audio review, or comprehensive board audit.

Verified Boyd and Vandenberghe, section 3.1.4, printed page 71, and section 5.5.3, printed pages 243–244; the cited Hessian and convex KKT qualifications agree with the chapter. Verified the SciPy scalar-minimization API distinction between bracket search and finite bounds. Princeton's directly fetched pages returned 403, but its indexed primary-source text confirmed the nonnegative-weight Dijkstra contract and DAG scheduling material. The general approximation-ratio definition was checked in the MIT PDF before the citation replacement.

The source-specific limitations remain explicit in the chapters. No human expert certification or comprehensive audiovisual fidelity is implied.
