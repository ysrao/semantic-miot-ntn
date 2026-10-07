# SPACOMM 2027 revised manuscript — the 10 yellow [AUTHOR:] notes, resolved

**Document:** `SPACOMM_2027_Semantic_mIoT_over_NTN___Revised_Manuscript__PDF.pdf`
("Task-Oriented Semantic Reporting for Massive IoT over Non-Terrestrial Networks:
A Trace-Driven Evaluation for Remote Agriculture and Flood Warning", 7 pages,
exported from LibreOffice 2026-10-06 16:31 UTC.)

**Correction to the earlier chat claim:** the PDF is NOT clean. It contains zero
PDF *annotation objects*, but 10 `[AUTHOR: ...]` notes are baked into the page
content as yellow-highlighted text on pages 4–7 (verified by pixel scan:
pp. 4–7 carry 3.9k–16.9k yellow pixels each; pp. 1–3 clean). All numbers below
were verified against `~/workspace/ntn-eval/results/*.csv` and `src/ntn_eval/`.

**No editable source of this revised manuscript exists in the workspace**
(the Oct-1 `build_paper.py` generates a different manuscript titled
"From Illustrative to Measured..."). The user must share the .docx/.odt or
apply these edits in LibreOffice.

---

## Note 1 (p.4) — cite parameter sources (IMD monsoon statistics, agronomic data)
**Status: fix ready.** Add to references:
> D. S. Pai, L. Sridhar, M. Rajeevan, O. P. Sreejith, N. S. Satbhai, and
> B. Mukhopadhyay, "Development of a new high spatial resolution (0.25° × 0.25°)
> long period (1901–2010) daily gridded rainfall data set over India and its
> comparison with existing data sets over the region," *MAUSAM*, vol. 65, no. 1,
> pp. 1–18, Jan. 2014, doi: 10.54302/mausam.v65i1.851.
Verified: IMD's own CMPG page (https://imdpune.gov.in/cmpg/Griddata/Rainfall_25_NetCDF.html)
instructs authors to cite Pai et al. (2014) for this product.
Suggested sentence next to the note: "Monsoon-phase stratification follows the
IMD 0.25° gridded rainfall climatology [new ref]; crop-stage soil-moisture
thresholds and the 500 mm root-zone bucket are stated model assumptions
(`src/ntn_eval/traces.py`)."

## Note 2 (p.4, §IV.C) — 1.28 kb/s sensitivity case or justify
**Status: justification ready with numbers (no re-run needed, but one is offered).**
At 1.28 kb/s single-tone, payload airtime scales ×12.5:
T_msg,raw = 2 + 0.13×12.5 = 3.63 s; T_msg,sem = 2 + 0.0578×12.5 = 2.72 s.
G_air = 3.63/(0.0528×2.72) ≈ **25.2×** vs the reported 19.6× — the 16 kb/s
multi-tone figure is *conservative*; gains grow at the lower rate because the
raw mode's larger payload suffers more. 90-day energies scale on the Tx term
only: raw 28.3→30.9 kJ, semantic 286→346 J (agri); saving 99.0%→98.9%.
Suggested insertion: "The 16 kb/s multi-tone assumption is conservative for the
reported gains: at the 1.28 kb/s single-tone rate of [18], G_air rises to
≈25× and the 90-day energy saving is unchanged at ≈99%, since the raw mode's
larger payload bears proportionally more of the slower rate."
If the reviewer insists on a full case: one-line change `rate_bps: 1280` in
`configs/ntn.yaml`, re-run `run_all.py` (~2.5 min).

## Note 3 (p.4, §IV.D) — public repository URL, archived DOI, commit hash
**Status: NOT satisfiable today — user decision required.** `~/workspace/ntn-eval`
is not a git repo, not on GitHub, has no DOI. Two options:
(a) soften the claim now: "available from the authors on request";
(b) publish: `git init` + push to GitHub + free Zenodo DOI (≈10 min, needs his accounts).
Recommend (a) for the Dec-28 submission draft, (b) before camera-ready.

## Note 4 (p.4, §V.B) — "first-attempt load is 0.22 Erlang"
**Status: reviewer mistaken; paper's 0.9 is the sim's own number.** The "2 s" is the
random-access/setup overhead *per attempt*, not the full slot. The simulator's slot
is T_RA + T_msg = 2.0 + 2.13 = 4.13 s → 217.9 slots/pass; R_pass = 100 reports →
first-attempt G0 = **0.46**; truncated-retry fixed point G = **0.89 ≈ 0.9** ✓.
Verified in `results/stage2.csv` (env, raw, M=50: G0=0.4608, G=0.8943,
mean_attempts=2.43). Fix = rewording only: "a 2 s random-access/setup overhead
per attempt (full slot ≈4.1 s including the ~2.1 s message at 16 kb/s),
giving 0.46 Erlang first-attempt, ≈0.9 Erlang with retries."

## Note 5 (p.5, §V.C) — define onset; confirm early decisions count as hits
**Status: fix ready (wording only).** Onset = first sample of each labeled event
episode in the trace generator: irrigation = soil moisture first stays below the
crop-stage threshold; flood = burst start (`traces.py`: "Ground-truth events are
these actuation onsets"). YES, early decisions count as hits: an episode
overlapping [onset, onset+D] whose trigger is delivered no later than onset+D
scores a hit (`stage3.py` docstring: "a latch already held from a slightly early
firing still covers the event"); detection delay is reported signed so earliness
stays visible instead of being hidden.

## Note 6 (p.5, §V.C) — GTO 104.6× vs 114.7 from (10)+Table I
**Status: real discrepancy, resolved — needs an estimator sentence + spread.**
104.6 = mean of per-seed (recall_sem/recall_raw)×G_air over seeds 202–205;
seed 201 dropped (raw recall = 0 → ratio undefined). Per-seed values:
156.2, 57.5, 117.4, 87.3 → **104.6 ± 42.2 (n=4)**. The reviewer's 114.7 is the
ratio of the reported table means (0.928/0.157×19.4); it differs because raw
recall swings 0–0.29 across seeds. Verified in `results/stage3.csv`.
Suggested insertion: "G_TO is computed per seed as (recall_sem/recall_raw)×G_air
and averaged over seeds with non-zero raw recall (seed 201 excluded, raw recall
0); the ratio of the table means (114.7) differs because the raw baseline's
recall varies 0–0.29 across seeds."

## Note 7 (p.6, Table III) — "SDs omitted where below 0.01: confirm or add"
**Status: real error — the caption claim is false; add the SDs.** Measured SDs
across 5 seeds (`results/energy.csv`): event-triggered 25.8 J (agri) / 24.0 J
(env); semantic 0.3 J / 1.0 J; raw and compressed SD = 0 (deterministic).
Replace caption with: "Event-triggered 1,566 ± 26 J (agri) / 291 ± 24 J (env);
semantic 286 ± 0.3 J / 374 ± 1.0 J; raw/compressed deterministic (SD = 0)."

## Note 8 (p.6, §V.E) — confirm delivery assumption (threshold update)
**Status: confirmed from code; state it.** The drift experiment assumes the
downlink threshold update is delivered with probability 1 ("Ideal delivery",
`run_all.py::_threshold_update_score` docstring); its airtime is included in the
reported kB/day. Suggested sentence: "The single downlink threshold update is
assumed delivered (downlink delivery not modeled); its airtime is included in
the kB/day figures."

## Note 9 (p.7, ref [9]) — add issue, pages, DOI
**Status: fix ready.** Replace with:
> L. X. Nguyen, A. D. Raha, P. S. Aung, D. Niyato, Z. Han, and C. S. Hong,
> "A contemporary survey on semantic communications: Theory of mind, generative
> AI, and deep joint source-channel coding," *IEEE Commun. Surveys Tuts.*,
> vol. 28, pp. 2377–2417, 2026, doi: 10.1109/COMST.2025.3616973.
(Issue number not shown on the publisher record viewed —
https://khu.elsevierpure.com/en/persons/choong-seon-hong/ lists vol. 28,
pp. 2377–2417; vol+pages+year+DOI is sufficient for the reference.)

## Note 10 (p.7, ref [19]) — institution, city, URL
**Status: fix ready (institution inferred, flagged).** Replace with:
> D. Richter, "Practical performance analysis of NB-IoT across terrestrial and
> non-terrestrial networks," Bachelor's thesis, Hochschule für Technik,
> Wirtschaft und Kultur Leipzig (HTWK Leipzig), Leipzig, Germany, 2026.
> [Online]. Available: https://theinternetofthings.eu/wp-content/uploads/2026/03/Bachelor-Thesis-2.-Practical-Performance-Analysis-of-NB-IoT-across-Terrestrial-and-Non-Terrestrial-Networkspdf.pdf
Institution verified inside the thesis text (measurements "deployed on the
rooftop of the Faculty of Digital Transformation at Hochschule für Technik,
Wirtschaft und Kultur Leipzig"); thesis title page not legible in extraction,
so confirm against the title page before submitting.
