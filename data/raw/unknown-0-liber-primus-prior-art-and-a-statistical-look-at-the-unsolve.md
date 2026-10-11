# Liber Primus: Prior Art and a Statistical Look at the Unsolved Pages

Research note, October 10, 2026

## Summary

- Prior art is extensive. The community has built open toolkits, transcriptions and "ruled-out" ledgers, so the cheapest first step is reading what has already failed.
- The solved pages share one framework: arithmetic on the 29 runes (mod 29), keys that are a word or a number sequence, and a consistent rule for the rune F.
- The unsolved pages are statistically different from every solved keyed page. Same-rune repeats are about five times rarer than chance (0.66% against 3.45%), while everything else looks random.
- That suppression is real (checked against two transcriptions and the page images), applies to the continuous rune stream, behaves like resampling rather than a fixed nudge, and leaks at a constant rate with no positional or contextual pattern.
- These tests characterize the text. They do not reveal the cipher.

## 1. Prior art

**Status.** Sources disagree on page numbering and counts. Community summaries split the book into LP1 (17 pages, all solved) and LP2 (58 pages, of which only pages 56 and 57 are solved), leaving 56 unsolved. A DEF CON 31 talk by members of the Cicada Solvers community described a Discord server of about 7,000 people as the main hub.

**Where the material lives.**

- scream314/cicada3301 on GitHub: page images and a rune transcription.
- jens-wedin/liber-primus on GitHub: the control-validated toolkit used for this note.
- The Uncovering Cicada wiki: frequency analysis, "how the solved pages were solved", and idea lists.
- Several recent GitHub archives that catalog ruled-out attacks. These are recent and I have not independently verified their claims, so treat them as leads.

**Documented as ruled out** (per the toolkit, each with a positive control): plain substitution, shifts and Atbash; repeating-key Vigenère; prime and totient keystreams; autokey; running keys from named texts (KJV, Liber AL, the Mabinogion, Blake, Emerson and others); short or mangled word keys; affine ciphers; and seeded pseudo-random streams. Other archives add derived keystreams and public "pads" such as Bitcoin, the NIST Beacon and RANDOM.ORG.

A useful standard from these projects: an attack counts as dead only if the same code first recovers a known answer (a positive control).

## 2. The solved pages

Reproduced with the toolkit's validator (9 of 9 checks pass). File numbers are the scan numbers.

| Pages | Method | Key |
| --- | --- | --- |
| 05, 10, 13, 16, 74 (page 57) | plain Gematria, no encryption | none |
| 06 to 09 | Atbash, then shift by 3 | none |
| 03 | Vigenère | DIVINITY |
| 14 to 15 | Vigenère | FIRFUMFERENFE |
| 73 (page 56) | shift by a running stream of (prime minus 1), mod 29 | totients of primes |

Page 4 is also reported to be a 1033 magic square, unencrypted.

**Shared structure.**

1. Every method is additive or a reflection on the integers 0 to 28 (rune index mod 29). Atbash is the map x to 28 minus x. Nothing solved needs a true matrix operation such as a Hill cipher.
2. Keys are meaningful: a word echoing the book's vocabulary, or a number-theoretic sequence.
3. In all three keyed methods the toolkit's model has a plaintext F stay a literal F and consume no key. That model reproduced the ciphertext exactly (251 of 251, 319 of 319 and 85 of 85 runes). The wiki's skipped indices (49 and 56) are consistent with F positions.
4. Complexity climbs in steps: no key, then a visible word, then a hidden number sequence.

## 3. Statistical fingerprint of the unsolved pages

Data: 12,942 adjacent rune pairs across the unsolved segments.

| Measure | Unsolved | Reference |
| --- | --- | --- |
| Same rune twice in a row | 86 pairs (0.66%) | random text 3.45% |
| Same measure, solved keyed pages (03, 14, 73) | about 3.1% (25 of 795) | random 3.45% |
| Index of coincidence (relative to random) | about 1.00 | random 1.00 |

So the unsolved text is flat like random text, but repeats are suppressed to roughly 19% of the chance rate. The solved keyed pages show nothing like it.

## 4. Tests and results

| Question | Result |
| --- | --- |
| Does suppression respect word or line boundaries? | No. Repeat rate is 0.63% inside words, 0.81% across word breaks, 0.62% across line breaks, so it acts on the continuous rune stream. |
| Fixed nudge or resampling? | Resampling. A "+1 on collision" rule would put the step +1 at 6.9% in simulation; observed is 3.54%, matching rejection. The simulated nudge was detectable, so the test has power. |
| Ciphertext-autokey? | Ruled out. English plaintext would make differences between neighbors strongly non-uniform (chi-square about 11,000 in a control). Observed is 41 against 27 degrees of freedom; pure random gives about 31. |
| Longer-range structure? | Coincidence at lags 2 to 12 is flat (about 3.45%). Lag 11 dips to 2.96% (z about -3.0), borderline after ten comparisons. |
| Where do the 86 leftover repeats fall? | No pattern. Permutation tests found nothing for position mod 2 to 64 (local or global), prime positions, nearness to F, per-segment variation (chi-square 6.7, 9 df), or repeated gaps (p 0.08). |
| Does repeat chance depend on context? | No detectable dependence on the previous rune (p 0.55), rune two back (0.68), previous step (0.47), a prior repeat (0.66) or the rune three back (0.78). Previous step in the lower versus upper half gave p 0.07, not significant across six tests. |
| Power of the context test | 91% to detect a planted 4x boost on 3 of 29 previous runes. Weaker effects (about 2x or less) could hide with only 86 events. |

## 5. Are the 86 repeats real?

- The two independent transcriptions (rtkd and the one the toolkit uses) agree on 15,744 of about 15,750 runes, and both contain all 86 repeats. The only disagreement inside the unsolved text is a single rune that does not touch a repeat.
- I cropped a random 14 repeats from the page scans (from pages where line matching worked). All 14 show two identical glyphs, including pairs split by a word dot or clause mark.
- A clean 14 of 14 puts the genuine share at 81% or more (one-sided 95% bound). Even if every remaining one were a misread, the rate would stay near 0.5%, far below 3.45%.

## 6. Interpretation

The unsolved text behaves like a stream in which each would-be repeat survives with probability about 0.19, independent of neighbors, position or segment. One reading is that roughly 19% of positions escape the rule while the rest obey it. That is speculation, because I cannot identify which positions escaped.

Any proposed mechanism has to reproduce: near-uniform steps between neighbors, flat long-range statistics, resampling-style suppression on the continuous stream, and a memoryless leak with no positional signal.

## 7. Limits

- Everything here is statistics on ciphertext. The text is close to uniform, so these tests cannot prove a keystream exists.
- "Ruled out" means ruled out within the tested search space; negatives from other projects are English-register negatives.
- The image check covers 14 of 86 repeats, from pages where automatic line matching worked (20 of 42 pages with repeats). It does not tell us whether real repeats were missed.
- Both transcriptions come from the same page images, so a shared misreading is possible, though the 14-of-14 image check makes it unlikely to matter.
- Several cited archives are recent and unverified.

## 8. Reproducing this

A zip of the scripts accompanies this note. Setup: clone jens-wedin/liber-primus, and sparse-clone scream314/cicada3301 (the assets/2014/liber-primus-complete folder) for the images. Paths in the scripts assume /home/claude. Run order: noreap.py, mc.py, more.py, where.py, xcheck.py, context.py, then sheet.py and sheet2.py for the image crops.

## 9. Possible next steps

These are suggestions, not findings.

- Test the "fraction of positions escape the rule" idea more directly, for example by checking whether escapes could coincide with F-like literal handling.
- Check the artwork-based section split some solvers have proposed against the repeat rate.
- Extend the cipher search to Hill-style matrix operations mod 29 on the unsolved text, using the repeat-suppression statistics as a constraint.
