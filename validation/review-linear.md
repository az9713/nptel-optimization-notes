# Independent review: chapters01–05

## Verdict

Accepted for mathematical, pedagogical, and code correctness at the exact SHA-256 hashes in `review-linear.json`. Runtime completion remains a separate root/CI release gate. All five manuscripts, metadata files, and labs were read end to end; no unresolved manuscript or code defect was found.

## Blocking defects

None remain in the reviewed files. A citation gap in the chapter05 Hungarian-method example was closed by the author during review: the general matching-cover assertion was replaced by a direct two-edge matching lower bound and an explicit two-line cover. That local certificate is sufficient for the worked example and was independently checked.

## Clarity and mathematical checks

The persistent workshop example has primal optimum (1,3), profit 9, and matching dual prices (1,1). The simplex reduced-cost and ratio signs are consistent with maximization. The phase-I example has optimum (1.5,0.5), cost 2.5. Chapter03 correctly limits its shadow-price formula to the basis-valid interval, and its rank-one inverse update has the required nonzero denominator. Chapter04 keeps a complete live-node queue: the LP bound 21 and integer incumbent 20 are justified, and neither a smaller bound than a competing live node nor a promising child alone licenses pruning. Its Gomory and mixed-integer cut derivations retain their distinct integrality assumptions. Chapter05 preserves zero-flow basis edges, decreases transportation costs 36→30→27, and supplies both shipping and assignment dual certificates. All 30 exercise solutions were checked.

## Structure and source scope

The chapters form a coherent progression from formulation and LP geometry through simplex, duality, integer optimization, and transportation/assignment. Each has six worked exercises, a deterministic lab, and timestamped lecture links. The original author supplied the full sequential source-reading records. This independent review checked selected primary references and the lecture12 pruning correction against captions around 1740–1900 seconds; it did not reread all lecture01–15 captions or perform a comprehensive audiovisual audit. Verified references include [Goemans LP notes](https://math.mit.edu/~shor/18.310/lpnotes310.pdf) chapter4 and the Bland rule section, [ETH discrete optimization notes](https://people.inf.ethz.ch/gaertner/subdir/teaching/lecture_notes/do.pdf) §8.2, and [SciPy linprog documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html).

## What works and execution evidence

The strongest feature is the use of small, inspectable certificates: dual resource prices, reduced costs, branch bounds, valid cuts, tree-edge potentials, and assignment row/column offsets. These make numerical answers auditable and distinguish local algorithmic steps from global optimality claims. Code review found the labs consistent with those contracts. The author reports completed 01–04 tests; the author 05 process 60424 and the reviewer combined01–05 process 61561 were pending when this receipt was written. Their completion is not claimed here. Root/CI must observe execution of the exact accepted lab files before release.

## Line-ending normalization

Root normalized chapter02 from CRLF to LF. The reviewer verified that replacing every CRLF pair in the saved prior file with LF yields the current file exactly. Only the chapter02 Markdown accepted hash was rebound; the scientific text and the other14 accepted files are unchanged.
