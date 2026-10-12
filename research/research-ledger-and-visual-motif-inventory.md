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


## Provenance-tool implementation review (2026-10-11)

Reviewed the connected private repository `invictustitan2/lp-annotation`, branch `master`, specifically `app/images.py`, `app/geometry.py`, `app/static/viewer.js`, `app/static/viewer.html`, `app/annotations.py`, `app/database.py`, `app/library.py`, and `app/exports.py`.

### Verified implementation behavior

- `app/images.py::inspect_image` opens the source, validates supported image format and dimensions, and computes SHA-256 over the original file bytes.
- `verify_source_unchanged` compares current SHA-256 and dimensions to expected metadata; `extract_crop` can require those expected values and extracts from the original image with Pillow using the recorded rectangle.
- `app/geometry.py::Rectangle` uses integer, half-open source-pixel coordinates `(x0, y0, x1, y1)`; right and bottom edges are excluded.
- In the browser UI, `sourcePoint(event)` maps pointer coordinates through the displayed image's bounding rectangle into `naturalWidth`/`naturalHeight` coordinates. `finalizeSelection` rounds each bound to an integer, clamps it to image dimensions, rejects empty rectangles, and records the resulting coordinates in browser state.
- `renderCrop` draws the selected source-image rectangle into a canvas of exactly `(x1-x0) × (y1-y0)`. Export serializes that canvas as PNG. Therefore the exported PNG is a derived/re-encoded crop, not a byte-preserving segment of the original file.
- The export filename embeds the rectangle as `crop-x0-y0-x1-y1.png`. The inspected viewer code does not embed the original SHA-256, source-image ID, application version, or crop rectangle in PNG metadata, nor does it create a dedicated persistent crop-provenance record at export time.
- Separately, saving a rectangle as an annotation stores its source-image ID, rectangle, observation/interpretation/status, and revision history in SQLite. That is a durable source-linked region record, but it is not proof that a particular exported PNG came from that region unless the filename, dimensions, pixels, and source record are independently matched.
- The local runtime data directory is `~/.local/share/lp-annotation/`; the database and original source files are intentionally outside the source repository. The GitHub repository therefore provides the implementation, not the local page-57 database record or its original scan bytes.

### Consequence for page-57 crop verification

The implementation establishes how a crop *would* be generated, but it does not by itself establish which exact rectangle generated the currently analyzed page-57 crop. The known working crop hash `5d7e7e667d55ed9a44f22e486c462bdea43cdd7fae6ecbddc7d26900649d1c4a` identifies the crop file, not its source rectangle. The canonical source scan is recorded in the research context as SHA-256 `3f5af995b39f94f268d4aa94825a10f2429f4a3affa1921a7f627e6d1bfcfb69`, dimensions 2400×3600, but the local annotation database has not been queried in this review.

To close the chain of custody without guessing, obtain a read-only export of the relevant local source-image row and page-57 region row/revisions from `~/.local/share/lp-annotation/annotations.sqlite3`, plus the crop file itself if pixel-level comparison is needed. Match source ID, source hash, source dimensions, rectangle, crop dimensions, and crop hash. Do not infer the rectangle from the crop filename alone or treat the canvas-exported PNG as the original scan.

### Status

Implementation review complete; page-specific crop provenance remains unverified pending the local database record. No original scan, trace points, or fit results were modified.


### Page-57 database check (user-run, 2026-10-11)

The user queried the local SQLite database read-only using the canonical source ID `3f167f8e-8aae-48ce-85a7-4e4f2e6b0794`. The source record matches the expected scan metadata above. The query returned **zero rows** from `regions` for that `source_image_id`; therefore no region rectangle or region revision is currently recorded for page 57. This is a verified absence in the queried database, not evidence that the crop itself is invalid.

Inspection of `app/static/viewer.js` confirms that pointer selection coordinates are mapped from the displayed image to natural/source pixel coordinates, rounded and clamped to integer bounds, then drawn from the image into a canvas. The crop export downloads a PNG named `crop-x0-y0-x1-y1.png`. The source selection exists in client-side state until a region is explicitly saved; exporting the PNG does not save a region. Thus a filename can encode a candidate rectangle, but only matching the crop file, its dimensions, and the canonical source pixels can validate that association.

Next verification: compute SHA-256 and dimensions for the exact working crop; parse the four integers from its original export filename if preserved; independently extract that rectangle from the canonical original scan using `extract_crop` with the recorded source hash/dimensions, encode to PNG, and compare decoded pixel arrays with the working crop. A pixel match establishes the rectangle despite the absent database region; a mismatch requires investigating resize/re-encoding or a different rectangle. Do not create a retrospective region record and represent it as contemporaneous provenance.


### Page-57 crop pixel verification — completed (2026-10-11)

The user ran the verification locally against the actual application implementation from the project parent directory. Results:

- Source record ID: `3f167f8e-8aae-48ce-85a7-4e4f2e6b0794`
- Source SHA-256 verified: `3f5af995b39f94f268d4aa94825a10f2429f4a3affa1921a7f627e6d1bfcfb69`
- Source dimensions: 2400×3600
- Candidate rectangle: `(160, 2246, 461, 2482)`, half-open source-pixel bounds
- Working crop dimensions: 301×236
- Working crop SHA-256: `5d7e7e667d55ed9a44f22e486c462bdea43cdd7fae6ecbddc7d26900649d1c4a`
- Crop re-extracted from the canonical source through `app.images.extract_crop`, with expected source SHA-256 and dimensions supplied: 301×236
- Decoded RGB pixel arrays: exact match (`ImageChops.difference(...).getbbox() is None`)

This resolves the specific crop/source association: the working crop is exactly reproducible from the canonical original using the candidate rectangle. The missing SQLite region row remains a true gap in contemporaneous database provenance, but does not invalidate the now independently verified crop. Record the rectangle as retrospectively verified by pixel comparison, not as a region that had been saved at crop time.

This verification supersedes the earlier “page-specific crop provenance remains unverified” status above. Historical notes are retained to preserve the audit trail; current status is **source, rectangle, crop dimensions, hash, and pixels verified**.

Next geometric step: visually inspect the already-generated local trace audit overlay before changing the 21-point trace. In particular, resolve the flagged near-180° angular step between points 0 and 1 by checking point placement and trace direction against the crop itself. Do not use the better numerical fit as a reason to alter points without visual evidence.

## Page-57 workflow and geometry correction (2026-10-11)

**User clarification:** point 0 `(176.048, 124.437)` is a manually placed fixed center/reference, not a curve sample. Points 1–20 are the 20 spiral samples. For fixed-center model comparisons, hold point 0 fixed and evaluate only points 1–20. Earlier text describing point 0 as a likely bad tracing click or as a curve sample is superseded for this analysis and must not be repeated as current fact. The submitted CSV/JSON remain unchanged.

**Completed fixed-center radial-log baseline (user-reported; do not rerun):** free slope `-0.17831`, golden-constrained slope `-0.30635`; RMS log-radius residuals `0.26060` and `0.43509`; multiplicative RMS factors `1.298×` and `1.545×`; quarter-turn growth `1.323×` and `1.618×`; angular span about 1.58 turns for both. This metric is radial log-space, not orthogonal pixel distance.

**Execution boundary:** the user runs all local commands, scripts, numerical analysis, and local output generation/inspection. The assistant must not use local execution tools, claim to inspect local-only outputs, or create unrequested scripts, branches, reports, commits, or PRs. Read `WORKING_CONTEXT.md`, this ledger, and relevant dated notes before acting; follow the recorded sequence and ask for local evidence only when it is necessary and not already supplied.

**Process incident:** an assistant-created branch `analysis/page57-fixed-center-orthogonal-comparison` contains an unvalidated, unrequested script `scripts/compare_page57_spiral_fixed_center.py`. It is not an approved deliverable and produced no validated results. No further changes to it should be made without explicit user instruction.
