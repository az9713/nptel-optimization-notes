# References and evidence limits

## Course identity and chronological spine

The [official NPTEL course page](https://nptel.ac.in/courses/111105039) identifies Optimization at IIT Kharagpur and the instructors, Prof. A. Goswami and Dr. Debjani Chakraborty. The [official syllabus](https://archive.nptel.ac.in/content/syllabus_pdf/111105039.pdf) lists the course topics. The supplied [YouTube playlist](https://www.youtube.com/playlist?list=PLbMVogVj5nJT8iTaUR8FoWBuJy0vs-Z3C) determines the exact recording inventory.

[source-manifest.json](source-manifest.json) records all 40 video identifiers, original titles, playlist positions, lecture numbers, listed durations, caption endpoints, track labels, acquisition times and SHA-256 digests. A digest identifies the acquired caption file; it does not certify the accuracy of its words or equations. Local captions are retained under the ignored working directory and are not redistributed.

## Primary mathematical references

[Stephen Boyd and Lieven Vandenberghe, *Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf), Cambridge University Press, 2004. Chapters 2–5 develop convex sets, convex functions, optimization models and duality. Chapters 9–11 develop descent, Newton and interior-point methods. The book’s treatment explains why a local optimality equation becomes a global certificate only under additional structure. Individual chapter references identify the topic-specific material used.

The [authors’ official book page](https://web.stanford.edu/~boyd/cvxbook/) provides the authorized download and errata. The book’s notation and sign convention may differ from a maximization LP in these notes; each chapter states the convention it uses.

The numerical laboratories use [NumPy](https://numpy.org/doc/stable/) and [SciPy](https://docs.scipy.org/doc/scipy/). Solver success alone is not used as a proof: labs check residuals, enumerate small alternatives or compare an independently derived value where appropriate. Software versions used for a release are recorded in the validation evidence.

## What the evidence establishes

All available English captions were acquired and read for the topic maps. The track metadata marks them non-automatic, and their last captions lie near the end of every recording. Endpoint coverage does not establish word-perfect completeness. Equations on slides or boards can be absent or corrupted in caption text.

The chapters therefore develop mathematics independently rather than presenting themselves as a visual transcription. Added numerical examples, proofs, counterexamples and implementation experiments are teaching constructions. Timestamp links associate a section with a related lecture interval; they do not claim that every sentence or example occurs in the recording.

Separate AI scientific review checks definitions, theorem assumptions, derivations, numerical constructions, exercise solutions and source mapping. Review receipts identify the exact chapter and lab hashes. This is bounded review, not human expert certification or formal verification. Mechanical checks separately cover executable code, source coverage, internal links, deterministic rebuilding, math rendering and reader controls.

## Attribution and local use

This is an independent educational edition. NPTEL, IIT Kharagpur, the instructors and the source authors retain their own work and are not claimed to endorse these notes. Recordings, captions, slides and downloaded reference books are linked or retained locally, not included in the public package. MathJax is bundled under its [Apache 2.0 license](assets/mathjax-LICENSE).

Open `index.html` locally or use the published reader. External recording and reference links require internet access. Print expands solution panels for study. The authored Markdown, chapter metadata, laboratory source and build/check tools remain available for inspection and revision.
