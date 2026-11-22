# Optimization study edition: editorial brief

Independent notes for NPTEL Optimization, IIT Kharagpur, course 111105039,
Prof. A. Goswami and Dr. Debjani Chakraborty. Source playlist has 40 recordings.
Full English caption tracks are local under work/transcripts/NN.txt and NN.json.
Raw captions stay local and must not be committed. source-manifest.json records
track metadata, duration, digest and original playlist position. Official lecture
numbers determine chapter reading order; lecture 40 is playlist position 35.

Reader: quantitatively mature, new to optimization. Define domain terminology,
state assumptions, show proof hinges and numerical checks. Chapters are original
exposition using lecture topic order, never a transcript paraphrase. Examples,
code and exercises are original teaching constructions, explicitly identified.

## Chapters and ownership

01: lectures 1–3, modeling and LP geometry.
02: lectures 4–7, simplex, Big M, two phase, degeneracy and exceptional cases.
03: lectures 8–10, duality, dual simplex, sensitivity.
04: lectures 11–12, integer programming.
05: lectures 13–15, transportation and assignment.
06: lectures 16–18, project networks, critical paths, PERT.
07: lectures 19–20, shortest paths and traveling salesperson.
08: lectures 21–22, differentiable unconstrained optimization.
09: lectures 23–24, equality constraints and KKT.
10: lectures 25–28, interval elimination, Fibonacci and golden section.
11: lectures 29–31, interpolation, direct and gradient search.
12: lectures 32–33, constrained numerical methods and penalties.
13: lecture 34, separable programming.
14: lectures 35–36, geometric programming.
15: lectures 37–38, dynamic programming.
16: lectures 39–40, multiobjective and multiattribute decisions.

## Authoring contract

Author chapters/chNN.md directly; renderer preserves authored text. Use $...$
and $$...$$ math. Each major topic heading carries a genuine caption-derived
YouTube timestamp link. Never infer a time from the title or fraction of duration.
Read every assigned caption sequentially, in bounded chunks without truncation.
Record section spans and lecture-specific distinctions in validation/source-read-NN.json.
Distinguish scope coverage from faithful reconstruction of board mathematics.

Comparable intellectual depth to work/exemplar-strong.md and exemplar-control.md:
connected prose, a persistent model, developed derivations, worked examples,
counterexamples, limitations, six fully solved exercises per chapter, and one
deterministic executable Python lab in labs/chNN.py. Code implements the stated
model and checks a meaningful numerical result; avoid trivial identity checks.
Each chapter should normally need 3000–5000 words; use subject-driven depth.
Code blocks can be standalone or read from the lab by the build tool.
Provide input/output contract and failure boundaries in prose. No unrun numbers.

Each author writes their chapter metadata to chapters/chNN.json with keys:
title, lectures (list of integer lecture numbers), objectives (3–5 strings),
prerequisites (string). No chapter prose in generators or Python string literals.

## Mathematical conventions and traps

For LP, state whether minimizing or maximizing, then fix reduced-cost signs.
Prefer max c^T x subject to Ax<=b, x>=0 and dual min b^T y,
A^T y>=c, y>=0. When using equality canonical form, explicitly introduce it.
Never infer integrality from integer coefficients; network matrices have a
specific integrality theorem. Never round an LP relaxation without checking.
KKT necessity needs constraint qualification; sufficiency needs convexity.
Distinguish stationary points, local extrema, global extrema and attainment.
PERT's normal approximation is a heuristic and merge/path correlation matters.
Golden/Fibonacci elimination requires a unimodal function and justified ties.
GP posynomials require positive variables and positive term coefficients;
monomial equalities only, and transform by logarithms.
DP state must capture information needed by future costs and transitions.
Positive weighted sums recover supported Pareto points; not all nonconvex
Pareto optima. Weighted decision scores depend on normalization/preferences.

## Primary references

Official course https://nptel.ac.in/courses/111105039
Official syllabus https://archive.nptel.ac.in/content/syllabus_pdf/111105039.pdf
Boyd and Vandenberghe, Convex Optimization (2004), §§2–5, 9–11:
https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf
For topic-specific references, browse primary sources and verify the actual
theorem/equation being used. No invented page numbers or uninspected citations.

## Review and evidence

The requested reference workflow requires separate author and scientific editor.
After authoring, another agent reviews all assigned chapters and labs. Authors
must not claim independent acceptance of their own work. Review results identify
exact paths, material defects, fixes, limitations and SHA-256 accepted bodies.
Full audiovisual audit and human expert certification are not claimed.
Keep independent review evidence in validation/; source-reading logs are public
metadata only, never large caption excerpts. Root owns build/UI/publication.
