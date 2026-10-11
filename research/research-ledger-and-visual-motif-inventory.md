# Liber Primus research ledger and visual-motif inventory

Created: 2026-10-11  
Status: initial archive inventory; not an interpretation of uninspected image details.

## Research discipline

Keep observations, measurements, interpretations, hypotheses, and conclusions in separate fields. Every proposed solve should identify:
- the exact source file/page and provenance;
- the operation or test, including parameters and code version;
- a positive control where applicable;
- the result and uncertainty;
- what result would falsify the hypothesis;
- links to related evidence without assuming one mechanism governs all pages.

Do not overwrite raw scans, submitted traces, or prior results. A failed test remains in the ledger with its scope and limitations.

## Existing material found in the parent archive

| Artifact | What it supports | Status / limitation |
|---|---|---|
| `data/raw/source-library/manifest.csv` | Provenance index for the canonical local scan library | Source paths are relative to `~/.local/share/lp-annotation/`; scans are not mirrored wholesale in this repo |
| `sources/transcription-master.txt` | Rune transcription with word/clause/paragraph/segment/chapter/page delimiters | Must be validated against page images for any exact local claim |
| `sources/index.txt` | Thematic page index from the existing project: page 20 “sprouts,” 25 “roots,” 57 “plants,” plus other labels | These labels are an index, not proof that illustrations encode a common system |
| `data/raw/unknown-0-liber-primus-page-image-repeat-check-cross-page-comparison.jpg` | Existing cross-page visual comparison | Inspect before creating a duplicate comparison |
| `data/raw/unknown-0-liber-primus-page-image-repeat-check-crop-page20.jpg` | Existing page-20 crop | Existing crop purpose is repeat checking; suitability for botanical-motif analysis unverified |
| `data/raw/unknown-0-liber-primus-page-image-repeat-check-crop-page66.jpg` | Existing page-66 crop | Existing crop purpose is repeat checking; suitability for botanical-motif analysis unverified |
| `data/raw/unknown-0-liber-primus-page-image-repeat-check-crop-page68.jpg` | Existing page-68 crop | Existing crop purpose is repeat checking; suitability for botanical-motif analysis unverified |
| `data/raw/unknown-0-liber-primus-page-image-repeat-check-crop-page74.jpg` | Existing page-74 crop | Existing crop purpose is repeat checking; suitability for botanical-motif analysis unverified |
| `data/raw/unknown-0-liber-primus-prior-art-and-a-statistical-look-at-the-unsolve.md` | Existing statistical-text and prior-art research | Separate from ornamental geometry; claims should be checked against its cited sources and scripts |
| `data/raw/page57-spiral/` | New working crop, manual trace, first fits, winding diagnostics and audit tools | Current geometric result remains exploratory; trace audit overlay is generated locally and not yet in Git |
| `sources/manual-pull/page20-guides.jpg`, `page66-guides.jpg`, `page68-guides.jpg`, `page74-guides.jpg` | Existing guide-marked page images | Need inspect their guide definitions before treating marks as source art |
| `sources/manual-pull/results.csv` | Existing tabular results from prior work | Column meanings and provenance should be documented before reuse |

## Visual-motif workstream

Start with pages already named in the existing index rather than assuming every page belongs to a single botanical family:

1. Page 57 (scan 57 / book page 40): dominant spiral and connected stem, current geometry target.
2. Page 20 (scan 20 / book page 3): index label “sprouts.”
3. Page 25 (scan 25 / book page 8): index label “roots.”
4. Page 74 (scan 74 / book page 57): index label “parable”; also reported in the existing research note as solved by plain Gematria. This is a potential text/image cross-check, not presumed to share the page-57 illustration method.
5. Pages 66 and 68: include because existing project already made repeat-check crops, not because a tree connection has been established.

The page index's labels are useful search handles only. Do not infer an iconographic or geometric relationship from the names alone.

## Per-page observation schema

For each relevant page, record:

- scan/page identifier and canonical source SHA-256;
- source image dimensions and any crop rectangle in source coordinates;
- visible motif components (loops, branches, roots, stems, junctions, endpoints, crossings);
- connectivity graph: nodes and edges, with ambiguous junctions marked;
- geometric measurements only after documenting a repeatable tracing/segmentation method;
- relationships to text, margins, rune blocks, or other page features;
- candidate explanations and at least one alternative;
- test, expected observation, observed result, limitations, confidence;
- links to other pages only when a measurable feature supports the link.

## Current page-57 geometry status

- New working crop SHA is recorded in trace metadata and verified by the audit script.
- Submitted trace has 21 manual points and remains immutable.
- The radial-pixel diagnostic reports a large angular step between points 0 and 1 for the exploratory free-fit center, and the two model fits imply different angular spans.
- The local overlay `data/raw/page57-spiral/trace_audit_overlay.png` should be visually inspected before any point is moved or removed.
- No validated conclusion about golden-ratio construction or symbolic intent has been reached.

## Existing theory ledger

The repository currently exposes the above source index and research notes, but no dedicated consolidated ledger of the user's separate tree/root theories was found among tracked files in the parent archive at this inventory pass. Do not treat that as evidence those theories do not exist; they may be in the local annotation workbench, nested toolkit repository, or prior conversation. When they are found, import them as separate entries without collapsing or rewriting them.

Suggested columns: `theory_id, original_statement, source_context, prediction, evidence_for, evidence_against, discriminating_test, status, confidence, linked_pages, linked_artifacts, revision_history`.
