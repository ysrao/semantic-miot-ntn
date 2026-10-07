# Compliance Note — SPACOMM 2027 Submission Package

**Paper:** "From Illustrative to Measured: Task-Oriented Semantic mIoT over NTN for Remote Agriculture and Environmental Sensing"
**Date prepared:** 2026-10-01 · **No external submission made** (package delivery is the end state)

## 1. Template recon (IARIA / SPACOMM 2027)

Sources: official CFP PDF (https://www.iaria.org/conferences2027/CfPSPACOMM27.pdf),
IARIA editorial rules (http://www.iaria.org/editorialrules.html), IARIA CfP boilerplate
(2025/2026 editions). Note: iaria.org HTML pages would not load in the fetch tool
(empty responses); facts below come from the CFP PDF plus search-indexed IARIA pages.

- **Venue:** 19th Int. Conf. on Advances in Satellite and Space Communications (SPACOMM 2027),
  Lisbon, Portugal, April 18–22, 2027.
- **Deadlines:** full-paper submission **Dec 28, 2026**; notification Feb 24, 2027;
  registration Mar 10, 2027; camera-ready Mar 14, 2027.
- **Track:** "Global coverage via 6G/7G: integrating 5G and IoT with satellite networks"
  (named in the introduction, per IARIA's rule to state the relation to conference topics).
- **Page limit:** final manuscripts 8.5"×11", **6 pages included in regular registration;
  up to 4 extra pages allowed at additional cost** (10-page hard max).
- **This manuscript: 8 pages** → 2 extra pages will incur additional fees at registration.
  Figures/tables/references all included in the count.
- **Format applied:** US Letter, two-column, 10 pt Times New Roman, single-spaced, justified,
  first-line indent, no page numbers; "Abstract - " (hyphen, per IARIA editorial rules —
  fixes the old "Abstract—" defect); "Keywords-" with ≤5 semicolon-separated terms ending
  in a period; figure captions centered 8 pt below figures; table captions 8 pt above tables;
  numbered references in order of first appearance. Submission accepts .pdf or .doc —
  both are delivered.
- **Review model:** IARIA does not publish a double-blind requirement; its editorial rules
  require author names, emails, and institutional addresses on the manuscript (consistent
  with single-blind review). **Authorship block is a placeholder** ("[Author names to be
  inserted]" etc.) — the author must complete names/affiliations/emails before submission.
  The original IEEE version was anonymized; nothing in this package is anonymized.

## 2. Verification checklist (done 2026-10-01)

- [x] **Citations ↔ bibliography:** programmatic audit — all 26 in-text citations [1]–[26]
  map to bibliography entries; all 26 entries are cited at least once; first-appearance
  order is strictly ascending.
- [x] **Tables:** 3 tables, all render full-width with header rows intact
  (Table I: Stage-1 accounting; Table II: Stage-3 task quality; Table III: energy).
- [x] **Figures:** 9 PNGs embedded, numbered Figure 1–9 in appearance order, each with a
  caption and an in-text reference. Fig. 1 is the redesigned architecture figure
  (new layout/style, not the IEEE version's).
- [x] **Proofread:** automated scan for double spaces / spacing-before-punctuation —
  clean (only equation-subscript false positives). Abstract rewritten; no references in
  abstract; abstract ends with a conclusion sentence; abbreviations avoided in abstract
  per IARIA rules.
- [x] **Bounded claims:** every gain number is qualified by application, trace type,
  task constraint, energy model, access configuration, and load range. No "capacity
  gain" / "beyond Shannon" language anywhere.
- [x] **Page size:** Letter (612×792 pt), confirmed in PDF metadata.

## 3. IEEE reviewer criticisms → how each is addressed

| # | Reviewer criticism | Addressed by |
|---|-------------------|--------------|
| 1 | No substantive experiments/simulations/traces/measurements/data | Three-stage trace-driven simulation; all headline numbers measured (mean±sd, 5 held-out seeds); link/energy models anchored in published NTN measurements [18][19] |
| 2 | Eq. (11) 32.5× was illustrative, treated as evidence | Retained but explicitly labeled "a teaching example, not a finding"; measured GB=42.6× reported separately in Sec. V |
| 3 | "Required Results" / forward-looking language = unfinished paper | Sec. V.B deleted; replaced with measured results; no future-tense experimental language remains |
| 4 | Five applications too broad | Narrowed to two (agriculture, environmental monitoring); other three condensed to one future-work paragraph (Sec. VI) |
| 5 | Missing task-quality, suppression, airtime, access-success, energy, device metrics | Tables I–III + Figs. 2–9: recall, P_miss, FA/week, detection delay, q, GB, G_air, M*, deadline success, full energy decomposition |
| 6 | Template/proofreading defects | Rebuilt from scratch in IARIA format; "Abstract—" defect fixed; full proofread pass |

## 4. Honest-negatives checklist (reported, not hidden)

- Env semantic recall 0.928 (not 1.0); residual 7.2% misses are access losses.
- Agri timing error 8 h in ALL modes (trace/rule property; reported as measured).
- Energy savings are congestion-amplified (≈95% uncongested vs 99% at load).
- Raw/compressed periodic reporting collapses to M*=0 for flood warnings.
- Dry-season tuner degenerates (zero flood examples); guarded update loop exists because of it.
- Traces are synthetic; energy figures modeled, not hardware; single LEO scenario;
  slotted-ALOHA, not NPRACH; device≡receiver rule.

## 5. Before submitting (author actions)

1. Fill in author names, affiliations, email addresses (title page placeholders).
2. Confirm the 8-page length is acceptable (2 extra pages at additional cost) or cut to 6.
3. Sanity-check the six author-flagged assumptions in RESULTS_SUMMARY.md
   (synthetic traces, modeled energy, single LEO scenario, slotted-ALOHA, deadlines).
4. Submit .pdf (or .doc) via the SPACOMM 2027 submission system before Dec 28, 2026.
   Dual submission is prohibited — SPACOMM 2027 is the single target.

## 6. Deliverables

- `SPACOMM2027_TaskOriented_Semantic_mIoT_NTN.docx` — submission manuscript (Word)
- `SPACOMM2027_TaskOriented_Semantic_mIoT_NTN.pdf` — submission manuscript (PDF)
- `build_paper.py` — reproducible builder (regenerates the .docx from sources)
- `COMPLIANCE_NOTE.md` — this file
