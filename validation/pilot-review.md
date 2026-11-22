# Independent scientific review: chapter 01

Verdict: ACCEPT for mathematical and pedagogical content. The quantitative reader
can reconstruct the LP, distinguish geometry from feasibility, prove the
basic-feasible-solution correspondence, and check the optimum with a certificate.
This is a separate reviewer from the author, applying science-editor against
EDITOR_DOMAIN.md. It is an AI review, not human certification or formal proof.

## Scientific checks

Read chapters/ch01.md, its metadata, labs/ch01.py, and the source-reading ledger.
Recomputed every stated workshop vertex, profit, capacity, staffing optimum,
rank example, and degeneracy exercise. The primal upper bound is the sum of
the two resource rows and is attained at (1,3). Both directions of the
vertex/basic-feasible-solution proof retain the full-row-rank and nonnegativity
hypotheses. The text correctly separates finite optimum, bounded feasible set,
existence of vertices, and uniqueness. The six solutions expose their reasoning.

Reviewed code for independent boundary intersection enumeration and SciPy
comparison, including infeasible and unbounded cases. The determinant tolerance
and dimensional restriction are explicitly limited in prose. Floating-point
vertex enumeration is not presented as a general LP classifier.

Checked source caption excerpts at lecture 2 1124–1160 seconds and lecture 3
560–620 and 1690–1740 seconds against the ledger. They confirm formulation,
convex-geometry terminology, and theorem transitions. Source repairs distinguish
a finite convex hull from a general polyhedron. This reviewer did not independently
reread all three recordings or inspect boards; full sequential caption reading is
the author's documented source pass.

## Depth and structure

Compared the complete chapter with both Stanford exemplars. It is shorter than
the regression exemplar and comparable in length to the policy-gradient exemplar,
but contains the relevant intellectual work: a persistent numerical model,
definitions before use, derived geometry, a two-sided structural proof, a
certificate, algorithmic checks, counterexamples, and worked solutions. No
length padding is needed for the pilot. Later chapters must retain this level
of explanation rather than imitate only its headings.

## Findings and repairs

No blocking scientific defects found. No author-body changes made. The lab link
is written in the root-reader convention used by chapter01; root's renderer
must resolve source Markdown links consistently across all chapters.

## Limits

No comprehensive audiovisual fidelity, independent external theorem audit,
human accessibility audit, or formal verification is asserted. Rendered-reader
and clean-export checks are performed separately by the project coordinator.
Accepted-body hashes are recorded in pilot-review-hashes.json; subsequent
substantive content changes require renewed scientific review.
