# NPTEL Optimization — independent study edition

**[Read the notes](https://az9713.github.io/nptel-optimization-notes/)** · **[Study guide](https://az9713.github.io/nptel-optimization-notes/study-guide.html)** · **[40-recording source map](https://az9713.github.io/nptel-optimization-notes/source-map.html)** · **[Interactive laboratory](https://az9713.github.io/nptel-optimization-notes/numerical-lab.html)**

Sixteen chapters covering all forty recordings in **Optimization, IIT Kharagpur**, by **Prof. A. Goswami and Dr. Debjani Chakraborty**: linear and integer programming, network models, nonlinear methods, geometric and dynamic programming, and multicriteria decisions. The edition includes **96 exercises with fully worked solutions**, **16 executable Python laboratories**, and an offline dark-mode reader.

[Official NPTEL course](https://nptel.ac.in/courses/111105039) · [Supplied YouTube playlist](https://www.youtube.com/playlist?list=PLbMVogVj5nJT8iTaUR8FoWBuJy0vs-Z3C)

## Chapters

| Chapter | Topic | Source lectures |
|---|---|---|
| [01](https://az9713.github.io/nptel-optimization-notes/ch01.html) | Modeling and LP geometry | 1–3 |
| [02](https://az9713.github.io/nptel-optimization-notes/ch02.html) | Simplex, artificial variables, exceptional cases | 4–7 |
| [03](https://az9713.github.io/nptel-optimization-notes/ch03.html) | Duality, dual simplex and sensitivity | 8–10 |
| [04](https://az9713.github.io/nptel-optimization-notes/ch04.html) | Integer programming, cuts and branch and bound | 11–12 |
| [05](https://az9713.github.io/nptel-optimization-notes/ch05.html) | Transportation and assignment | 13–15 |
| [06](https://az9713.github.io/nptel-optimization-notes/ch06.html) | Project networks, critical paths and PERT | 16–18 |
| [07](https://az9713.github.io/nptel-optimization-notes/ch07.html) | Shortest paths and traveling salesperson | 19–20 |
| [08](https://az9713.github.io/nptel-optimization-notes/ch08.html) | Stationarity, curvature and global optimality | 21–22 |
| [09](https://az9713.github.io/nptel-optimization-notes/ch09.html) | Equality constraints and KKT | 23–24 |
| [10](https://az9713.github.io/nptel-optimization-notes/ch10.html) | Interval elimination, Fibonacci and golden sections | 25–28 |
| [11](https://az9713.github.io/nptel-optimization-notes/ch11.html) | Interpolation, direct search and gradient descent | 29–31 |
| [12](https://az9713.github.io/nptel-optimization-notes/ch12.html) | Feasible directions, cutting planes and penalties | 32–33 |
| [13](https://az9713.github.io/nptel-optimization-notes/ch13.html) | Separable programming | 34 |
| [14](https://az9713.github.io/nptel-optimization-notes/ch14.html) | Geometric programming | 35–36 |
| [15](https://az9713.github.io/nptel-optimization-notes/ch15.html) | Dynamic programming | 37–38 |
| [16](https://az9713.github.io/nptel-optimization-notes/ch16.html) | Multiple objectives, AHP and TOPSIS | 39–40 |

Lecture40 occurs at playlist position35. The source map retains both playlist position and official lecture numbering; the reader follows the latter. No supplied recording is silently omitted or duplicated.

## What this edition adds

The recordings provide the topic sequence. The notes develop mathematical models, proof hinges, numerical examples, counterexamples, implementation contracts and full exercise solutions. Added material is distinguished from lecture discussion; reused numerical data are attributed. Timed links locate related discussions and do not imply that every added derivation occurs in the recording.

The treatment makes consequential assumptions explicit: LP objective and reduced-cost signs, valid integer pruning, PERT approximation limits, constraint qualifications for KKT, tangent-space curvature, unimodality for elimination, positive-variable GP forms, sufficient dynamic-programming states and the limits of weighted Pareto scalarization.

The interactive laboratory exposes LP resource prices and quadratic gradient conditioning. The Python labs check small algorithms against exact calculations, enumeration, residuals or an independent solver.

## Evidence and review boundary

All forty available English caption tracks were acquired and read sequentially. YouTube labels them non-automatic; that metadata does not ensure word-perfect transcription. Complete board/slide and audio review was not performed. The notes independently reconstruct mathematics rather than claiming a visual transcription or verbatim lecture account.

Separate AI scientific editors reviewed the chapters, derivations, worked solutions and labs. Review receipts bind acceptance to exact source and lab hashes. This is not human expert certification or formal proof verification. Mechanical and browser checks are separate evidence.

- [Source manifest](source-manifest.json): identities, durations, original positions, caption provenance and digests.
- [Production workflow](WORKFLOW.md): the older NPTEL/Stanford workflow used for this edition.
- [Package and code checks](validation/package-checks.json).
- [Desktop/mobile browser checks](validation/browser-checks.json).
- [Review receipts and source-free rebuild](validation/release-checks.json).
- [References and limits](https://az9713.github.io/nptel-optimization-notes/references.html).

This is an independent educational publication, not an official NPTEL or IIT Kharagpur edition or an endorsement. Source recordings and cited works belong to their respective creators. Recordings, captions, slides and downloaded reference books are not redistributed. Raw captions remain local in compact, digest-verified archives; temporary media and build files are removed.

## Use and rebuild

Download the repository ZIP, extract it, and open `index.html`. Mathematics, navigation, solution panels, code-copy controls and interactive experiments work offline. Recordings and external references require internet access. Print expands the solutions.

Authored Markdown and metadata live in `chapters/`; laboratories live in `labs/`. Python3.13 was used for this release.

```text
python -m pip install -r requirements.txt
python tools/build.py
python tools/check.py
python tools/release_check.py
```

For browser checks, install `playwright==1.57.0` and a Chromium browser, then run `python tools/browser_check.py`. Pass `--browser` with an installed Chromium or Edge executable when needed. GitHub Actions rebuilds and checks the committed package, including every page at desktop and phone widths, before deploying Pages.

The renderer uses a single local MathJax SVG bundle under its [Apache2.0 license](assets/mathjax-LICENSE); it has no rendering CDN, analytics, build dependency folder or video payload.
