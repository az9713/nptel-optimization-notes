# Production workflow

This edition follows the nine-pass workflow of the October 2026
[NPTEL Evolutionary Dynamics edition](https://github.com/az9713/nptel-introduction-to-evolutionary-dynamics-notes/blob/main/WORKFLOW.md)
and the September 2026 [Stanford CS229 edition](https://github.com/az9713/cs229-machine-learning-notes).
The local transcript-grounded-textbook, rigorous-explainer, analyze-sources and
science-editor instructions guide source reading, derivation and validation.

1. Inventory all supplied playlist entries and preserve upload positions and
   official lecture numbers independently.
2. Acquire English caption tracks, provenance and duration bounds. Retain raw
   transcripts locally under ignored work/, never publish recordings or captions.
3. Read sources sequentially and map actual timed topics before drafting.
4. Develop a dependency-respecting outline and stable chapter notation.
5. Write original explanations, worked constructions, six solved exercises and
   one tested numerical lab per chapter; verify external primary references.
6. Use separate authors and scientific editors. Repair findings and bind review
   receipts to current chapter and laboratory digests.
7. Audit course coverage, coherence and comparable intellectual depth against
   two older Stanford chapters. Report any remaining difference honestly.
8. Build an offline static reader. Check mathematics, links, code, controls,
   accessibility basics, and responsive desktop/mobile layout.
9. Inspect the public Git tree, perform a source-free rebuild, commit and push.
   Verify publication when available, then remove temporary acquisition/build
   files and media while retaining compact transcripts and durable evidence.

Chapter source: chapters/chNN.md and chNN.json. Labs: labs/chNN.py.
Build: python tools/build.py. Check: python tools/check.py.
Browser checks: python tools/browser_check.py (requires Playwright and Chromium).

The source course and recordings belong to their creators. This independent
edition adds its own mathematics and examples. Caption inspection does not
establish comprehensive fidelity to visual board equations or audio.
