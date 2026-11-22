# Independent course coherence review

Reviewer: `network_classical`. This is a bounded course-level pass following the chapter scientific reviews. It does not repeat every proof, rerun laboratories, certify the built browser package, or replace release checks.

Disposition: accepted. The reviewed support text accurately describes the course scope, counts, prerequisites, and evidence limits. No support-text correction is required for a material error. The minor source-ledger convention difference found during review has been resolved as documented below.

## Material checked

Read `README.md`, `overview.md`, `study-guide.md`, `references.md`, `source-manifest.json`, all 16 chapter metadata files, and all 16 source-reading ledgers. Rechecked exercise/solution structures and existence of the chapter laboratory files without rereading all proofs. Checked every YouTube watch link in the chapter manuscripts against the mapped lecture identifiers and recording duration.

The [official NPTEL course page](https://nptel.ac.in/courses/111105039) independently confirms Optimization at IIT Kharagpur and the instructors Prof. A. Goswami and Dr. Debjani Chakraborty. The local manifest supplies the recording inventory reviewed here; this pass did not reacquire the entire remote playlist.

## Coverage and count findings

- Chapter metadata contains lectures 1 through 40 exactly once, in official lecture order. All source-reading ledgers contain the same exact partition.
- The manifest contains 40 distinct lecture numbers, 40 distinct video identifiers and all playlist positions 1 through 40. Lecture 40 is at playlist position 35; lectures 35–39 occupy positions 36–40. The README explains this difference correctly.
- Total listed recording duration is 138,253 seconds, or 38.403611 hours. The overview's approximation of 38.4 hours is accurate.
- Every chapter has six exercise prompts and six worked solutions: 96 of each. Chapters 6–10 use numbered prompts and solutions in one disclosure panel, while the other chapters use individual exercise headings and panels. Counting only one panel format would undercount the actual content.
- Exactly one intended chapter lab, `labs/ch01.py` through `labs/ch16.py`, exists for each chapter. The claim of 16 chapter labs is accurate. This count is not an execution-success claim.
- Chapter YouTube watch links all reference a recording mapped to that chapter, and their linked timestamps lie within its listed recording duration.

## Prerequisites and course logic

The progression is coherent: LP geometry supports bases and dual certificates, which support integer bounds, transportation and assignment; network recurrences precede shortest paths and tours; calculus and curvature precede equality constraints, KKT and nonlinear methods. Interval elimination precedes interpolation and multidimensional line search. Separable and geometric programs explicitly require their additional structure. Dynamic programming distinguishes sufficient state and information timing. Multicriteria methods require preferences and scaling beyond mere dominance.

The metadata and study-guide paths state the necessary background without implying that familiarity with a solver supplies a mathematical certificate. Chapter 8 explicitly calls for multivariable calculus and symmetric-matrix eigenvalues; chapter 6 calls for elementary probability; chapters 14–16 identify logarithms, probability and eigenvector prerequisites as appropriate. No circular chapter dependency or missing critical prerequisite was found in this bounded pass. The proposed AI workload allocator is clearly labeled as an unevaluated exercise rather than an established production result.

## Evidence claims and limits

The public text distinguishes author caption reading from independent scientific review, numerical checks, browser checks and audiovisual review. It says that YouTube labels the tracks non-automatic without treating that label as a transcription guarantee. It identifies the publication as an independent reconstruction, distinguishes added constructions from timestamped lecture discussion, and denies comprehensive audiovisual audit, human certification and formal verification. These boundaries agree with the author ledgers and review workflow.

The statement that all captions were sequentially read is an author-attested production claim supported by the source-reading ledgers, not a claim that this reviewer repeated every source reading. Independent chapter reviews are performed by separate AI agents; they do not constitute human expert review. The final release still needs the separately recorded executable, rebuild and browser gates. This pass did not verify a remote deployment or all offline browser behavior.

## Resolved source-ledger convention

The first version of `source-read-01.json` through `source-read-05.json` recorded the final caption's start time, rounded to two decimals, as the upper `coverage_seconds` value. Comparing the underlying caption records confirmed this for all lectures 1–15. The owning author normalized these entries to the manifest's first-caption start and final-caption end, repeated each manifest transcript digest, and added an explicit coverage convention. The reviewer read the updated ledgers and checked these values. Topics, repairs and the author's source-reading attestations remain unchanged.

All 40 lecture entries now use consistent caption-span endpoints and identify the acquired transcript digest. This is a metadata clarification, not newly performed source reading or audiovisual verification. No ledger convention finding remains.

Also verified the final manifest normalization against the saved original bytes: replacing CRLF with LF produces exactly the current file, and parsed JSON content is identical. The original backup matches the reviewer's previously retained byte buffer. The manifest SHA-256 changed from `cc5b32f81c5c2f15e064fd1a18a057ace830a3b6460d5edc0334321b76b37932` to `d786cbe710848aea06ae1670605b9b87e8764eb340e66bfa1a10b210165dc867`; none of the 40 recording records changed.

The final byte audit also normalized `source-read-06.json` through `source-read-10.json` from CRLF to LF. Independently compared each saved original with its current file: CRLF-to-LF replacement reproduces the new bytes exactly, and parsed JSON content is identical. Refreshed only those five accepted hashes; the other 32 course hashes still match. The companion receipt records each before/after digest and verification result. No source-reading claim, timestamp, topic map or repair changed.

## Manifest interface addition

After the line-ending verification, `source-manifest.json` gained a `sources` interface containing one playlist identity and 40 recording aliases. Independently compared every original top-level field with the parsed original backup: all values, including the entire canonical recording inventory, are unchanged. `sources` is the only added top-level field. All 41 aliases exactly derive their identifiers, URLs, status and coverage scope from the canonical playlist and recording data; the caption-only and no-audiovisual-review boundaries remain explicit. The earlier pure-whitespace comparison describes the normalization step before this interface addition, not the expanded current manifest.

Read the generator and `artifact-manifest.json`. Its 38 unique output paths all exist as nonempty files inside the project: 16 chapter HTML files, 16 Python labs and six course-level outputs. Each chapter/lab pair has exactly the lecture dependency identifiers in its chapter metadata. Each course-level output has the playlist plus all 40 lecture identifiers. All dependency identifiers resolve to source aliases, without duplicates. These dependencies describe topic provenance, not a new claim that added teaching constructions occur verbatim in the recordings. Refreshed the current source-manifest hash and added the artifact-manifest hash; all 38 course accepted-file hashes match.

The companion JSON binds this pass to the reviewed support files, metadata and source ledgers. If those files change, update the receipt only after inspecting the changes.
