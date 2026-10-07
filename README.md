# NTN Task-Oriented Semantic mIoT — Trace-Driven Evaluation

Trace-driven simulation implementing the 3-stage evaluation protocol from
Section VII of *"Application-Specific Semantic and Task-Oriented Communication
for Massive IoT over NTN"*, comparing **semantic / task-oriented** reporting
against raw periodic, compressed periodic, and event-triggered baselines for
two applications: smart-agriculture irrigation decisions and flood warnings.

## Quick start

```bash
cd ~/workspace/ntn-eval
python3 src/ntn_eval/run_all.py
```

Runs end-to-end in ~2.5 minutes. Regenerates `results/` (CSVs) and `figures/`
(PNGs). Deterministic: all seeds fixed; re-running reproduces the numbers.

Requirements: Python 3, `numpy`, `pandas`, `matplotlib` (see `requirements.txt`).

## Layout

```
configs/        YAML: modes, agri/env traces, NTN link, energy model
src/ntn_eval/
  config.py     config loader
  traces.py     synthetic trace generators (soil moisture, river level)
  schemes.py    reporting-mode runners (raw/compressed/event/semantic)
  stage1.py     deterministic load accounting  (eqs 1–4, 6–8)
  stage2.py     NTN access Monte Carlo: slotted ALOHA + fixed point (eq 9)
  stage3.py     task rules, episode scoring, task-oriented gain (eqs 10–11),
                drift detector
  energy.py     device energy model (eq 5)
  stats.py      CI helpers
  plots.py      figure generators
  run_all.py    full pipeline: traces → tuning → stages 1–3 → energy →
                sensitivity → drift → figures
tests/test_stage1.py   9 unit tests incl. paper eq (11): G_B(200,20,60,0.1)=32.5
results/        all CSV outputs
figures/        fig1–fig6 PNGs
RESULTS_SUMMARY.md     headline numbers, ablations, caveats, assumptions
```

## What it measures

- **Stage 1:** offered load, admission ratio q, byte gain G_B and airtime gain
  G_air per mode (deterministic).
- **Stage 2:** NTN random-access Monte Carlo → deadline-success vs population M;
  supportable population M* at 95% success; burst robustness.
- **Stage 3:** end-to-end task quality (episode-based recall, miss probability,
  false-alarm rate, detection delay, timing error) at M = 100 devices/beam;
  task-oriented gain G_TO.
- **Energy:** eq (5) breakdown per device / 90 days + AI-cost break-even sweep.
- **Drift:** dry-season-tuned thresholds under monsoon shift; 3σ detector +
  threshold-update recovery.

Key design choices: device and receiver run the *identical* decision rule
(threshold + persistence + hysteresis + causal smoothing), so the comparison
isolates *where/when* bits are sent; thresholds are tuned on seeds 101–105 and
evaluated on held-out seeds 201–205; flood ground truth uses hysteresis latching
so multi-peak floods score as one event.

## Headline numbers (mean over 5 seeds)

- Semantic: q ≈ 0.05, G_B ≈ 42×, G_air ≈ 19×, 0.59 kB/device/day (vs 24.96 raw).
- M* (95% deadline success): agri 1600 (semantic) vs 50 (raw);
  env 400 (semantic) vs **0** (raw — collapses).
- Task recall at M = 100: agri 1.000 (all modes); env **0.928** (semantic) vs
  0.157 (raw), 0.657 (event-triggered). G_TO = 19.6× (agri), 104.6× (env).
- Energy/device/90 d: 286 J (agri) / 374 J (env) vs ~28 kJ raw (99% saving,
  congestion-amplified; ≈ 95% uncongested).

See `RESULTS_SUMMARY.md` for the full table, ablations, negative findings,
and the assumptions to sanity-check (modeled energy values; configured NTN
scenario; synthetic traces).
