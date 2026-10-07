# Results Summary — Trace-Driven Evaluation of Task-Oriented Semantic mIoT over NTN

**Generated:** 2026-10-01 · **Pipeline:** `src/ntn_eval/run_all.py` (deterministic; seeds fixed)
**Results:** `results/` (CSVs) · **Figures:** `figures/` (PNG)

This package implements the 3-stage evaluation protocol from Section VII of
*"Application-Specific Semantic and Task-Oriented Communication for Massive IoT
over NTN"* for two applications: (1) smart agriculture — irrigation decisions;
(2) environmental monitoring — flood warnings. It compares **semantic /
task-oriented** reporting against **raw periodic**, **compressed periodic**,
and **event-triggered** baselines. All numbers below are measured from the
simulation (mean ± sd over 5 held-out seeds, 201–205), not assumed.

---

## Headline results

### Stage 1 — Offered load / suppression (deterministic accounting)

| App | Mode | Reports/day | kB/day | q (admission) | G_B (byte gain) | G_air (airtime gain) |
|-----|------|------------|--------|---------------|-----------------|---------------------|
| agri | raw | 96.0 | 24.96 | 1.000 | 1.0 | 1.0 |
| agri | compressed 2:1 | 96.0 | 15.36 | 1.000 | 1.6 | 1.0 |
| agri | event-triggered | 35.1 | 9.12 | 0.365 | 2.7 ± 0.1 | 2.7 ± 0.1 |
| agri | **semantic** | 5.1 | 0.59 | 0.053 | **42.6 ± 0.1** | **19.6 ± 0.1** |
| env | raw | 96.0 | 24.96 | 1.000 | 1.0 | 1.0 |
| env | compressed 2:1 | 96.0 | 15.36 | 1.000 | 1.6 | 1.0 |
| env | event-triggered | 4.5 | 1.18 | 0.047 | 22.1 ± 5.2 | 22.1 ± 5.2 |
| env | **semantic** | 5.1 | 0.59 | 0.053 | **42.3 ± 0.2** | **19.4 ± 0.2** |

Decomposition (eq 8): G_B = (1/q) × (H+L_raw)/(H+L_x).
Agri semantic: 18.9× from report suppression × 2.25× from payload shrinkage
(260 B → 80 B). Env semantic: 18.8× × 2.25×.
Figure: `fig1_suppression_decomposition.png`.

### Stage 2 — NTN access: supportable population M* (deadline success ≥ 0.95)

Configured LEO scenario: 600 km, 48 passes/day × 900 s (ρ = 0.5), 180 kHz,
16 kbps, 2 s random-access slot, ≤ 3 attempts/pass with retries across passes.

| App | raw | compressed | event-triggered | semantic |
|-----|-----|-----------|-----------------|----------|
| agri (D = 6 h) | 50 | 50 (100 burst) | 200 | **1600** |
| env (D = 45 min) | **0** | **0** | 800 (400 burst) | **400** |

Raw/compressed **collapse to M* = 0 for flood warnings**: at even 50 devices/beam,
congested slotted-ALOHA access (G₀ ≈ 0.9 Erlang) cannot meet the 45-min deadline
with 95% reliability. Semantic supports 8× (agri) and infinitely more (env, where
raw supports none) devices per beam. Figures: `fig2_airtime_vs_load.png`,
`fig4a/b_task_capacity.png`, `fig6_burst.png`.

Burst robustness (5% of devices in one pass, M = 800): agri semantic holds
Pr(delay ≤ D) = 1.00; env semantic 0.93 → 0.75, event-triggered 0.96 → 0.81;
raw/compressed remain at 0.

### Stage 3 — Task quality at operating point M = 100 devices/beam

Device and receiver use the **identical** decision rule (threshold + 2-sample
persistence + hysteresis + causal moving-average smoothing); thresholds tuned on
seeds 101–105, evaluated on held-out seeds 201–205. Episode-based scoring:
a hit requires the decision delivered within the application deadline.

**Agriculture (irrigation, D = 6 h):**

| Mode | Recall | P_miss | FA/week | Mean det. delay | Timing err | G_TO |
|------|--------|--------|---------|----------------|-----------|------|
| raw | 1.000 ± 0.000 | 0.000 | 0.06 ± 0.07 | −5.1 h | 8.0 h | 1.0 |
| compressed | 1.000 | 0.000 | 0.06 | −5.9 h | 8.0 h | 1.0 |
| event-triggered | 1.000 | 0.000 | 0.09 | −7.9 h | 8.3 h | 2.7 |
| **semantic** | **1.000 ± 0.000** | **0.000** | **0.06 ± 0.07** | **−7.6 h** | **8.0 h** | **19.6** |

**Environment (flood warning, D = 45 min):**

| Mode | Recall | P_miss | FA/week | Mean det. delay | Timing err | G_TO |
|------|--------|--------|---------|----------------|-----------|------|
| raw | 0.157 ± 0.111 | **0.843** | 0.02 | +0.57 h | 0.84 h | 1.0 |
| compressed | 0.206 ± 0.128 | 0.794 | 0.02 | +0.49 h | 0.43 h | 1.5 |
| event-triggered | 0.657 ± 0.087 | 0.343 | 0.00 | +0.54 h | 0.35 h | 83.5 |
| **semantic** | **0.928 ± 0.068** | **0.072** | **0.03 ± 0.07** | **+0.51 h** | **0.28 h** | **104.6** |

G_TO = (recall_mode / recall_raw) × G_air (task-oriented gain, eq 10/11):
**19.6× (agri), 104.6× (env)**. The env ratio is large because the raw baseline
collapses under the tight deadline — reported as measured, not trimmed.
Figure: `fig3a/b_quality_vs_resource.png`.

> **Honest caveats (do not hide):**
> - Agri decisions arrive **5–8 h early on average** (negative detection delay,
>   8 h mean timing error) in *all* modes — a property of the slow soil-moisture
>   dry-down trace and the threshold rule, not of semantic reporting. For
>   irrigation this earliness is low-cost (asymmetric: early ≫ late), but it is
>   reported as measured.
> - Env semantic misses 7.2%: with ideal delivery the tuned rule has
>   recall = 1.0, so the residual misses are **access losses at M = 100**, not
>   decision errors.
> - Event-triggered env reaches recall 0.657 — a respectable cheap baseline;
>   semantic's edge is the extra 27 points of recall plus 19× airtime saving.

### Energy (eq 5, per device / 90 days, at M = 100)

| App | raw | compressed | event-triggered | semantic | Net saving S_E |
|-----|-----|-----------|-----------------|----------|----------------|
| agri | 28,275 J | 27,197 J | 1,566 J | **286 J** | **99.0%** |
| env | 28,310 J | 27,240 J | 291 J | **374 J** | **98.7%** |

Decomposition: raw's energy is dominated by **access retries under congestion**
(E_retx ≈ 25.8 kJ at M = 100 — the retry storm); semantic's by idle listening
(117 J) + sensing + AI inference. **The 99% figure is load-dependent**: at
uncongested load the saving from fewer transmissions alone is ≈ 95%.
Break-even: semantic still saves energy for AI inference costs up to
≈ 300 mJ (agri) / ≈ 100 mJ (env) — orders of magnitude above the modeled
0.1–1 mJ. Figure: `fig5_energy.png`.

> **Assumption to sanity-check:** all energy values are *modeled NB-IoT-class*
> figures (sensing 2 mJ, AI 0.1–1 mJ, access 250 mJ/attempt, TX 0.5 µJ/bit,
> idle 15 µW), **not hardware measurements**.

### Drift / threshold adaptation

Thresholds tuned on dry-season data only, evaluated on monsoon (env) / dry
(agri) held-out segments. A 3σ baseline-shift detector triggers a **threshold
update** (downlink push of the full-season threshold).

| App | Variant | Recall | P_miss | FA/week |
|-----|---------|--------|--------|---------|
| env | dry-tuned (stale) | 0.746 | 0.254 | 0.88 |
| env | **dry-tuned + update** | **1.000** | **0.000** | **0.08** |
| env | full-tuned (oracle) | 1.000 | 0.000 | 0.08 |
| agri | dry-tuned | 1.000 | 0.000 | 0.08 |
| agri | dry-tuned + update | 1.000 | 0.000 | 0.08 |

The stale env threshold (tuned with zero flood examples — the tuner degenerately
picked the most conservative offset, −0.6 m) causes both misses and false
alarms; one threshold update restores oracle performance at negligible cost.
Agri thresholds generalize across seasons (dry-tuned ≡ full-tuned).

---

## Ablation (where the gain comes from)

- **Admission (1/q)** dominates: 18.9× of the 42.6× byte gain (agri).
- **Payload shrinkage** (260 B → 80 B): 2.25×.
- **Header (60 B)** caps the airtime gain: G_air = 19.6 < G_B = 42.6.
  Sensitivity: H = 20/60/120 B → G_B = 55.2/42.6/34.5 (agri semantic);
  heartbeat K = 1/2/4 per day changes G_air by < 10%.
- **Event-triggered vs semantic:** event-triggered already captures most of the
  admission gain for env (q = 0.047, G_B = 22.1) but sends full raw payloads on
  trigger and, for agri, fires far more often (q = 0.365) because the trigger
  rule lacks the semantic's smoothing/hysteresis.

## Negative / break-even findings (reported, not hidden)

1. Raw/compressed periodic reporting **cannot support flood warnings at any
   modeled population** (M* = 0) — a hard negative for the conventional baseline.
2. Semantic's env recall is **0.928, not 1.0** — the 7% gap is access loss.
3. Agri timing error is **8 h** in all modes — the task rule fires early on slow
   dry-downs; semantic does not fix this (nor does it make it worse).
4. Energy savings are **congestion-amplified**; the uncongested saving is ≈ 95%.
5. The env dry-season tuner **degenerates** (no flood examples → most
   conservative offset); the fallback/update story exists because of this.

## Assumptions the author must sanity-check

1. **Energy values are modeled**, not measured (NB-IoT-class assumptions).
2. **NTN scenario is configured**: 600 km LEO, 48 passes/day, ρ = 0.5,
   16 kbps — a plausible but single scenario; no multi-constellation sweep.
3. **Traces are synthetic** (water-balance soil moisture; leaky-integrator
   river level) with calibrated noise — no real sensor datasets.
4. **Slotted-ALOHA access** with geometric retries; no power control,
   capture effect, or NTN-specific random access (e.g., NB-IoT NPRACH) modeling.
5. **Device ≡ receiver rule** by construction (no model mismatch); the semantic
   gain is from *where/when* data is sent, not from a smarter model.
6. Deadlines (6 h agri, 45 min env) and the 0.95 success criterion are
   application assumptions.

## Reproduction

```
cd ~/workspace/ntn-eval
python3 src/ntn_eval/run_all.py   # ~2.5 min; regenerates results/ and figures/
```

Requirements: Python 3, numpy, pandas, matplotlib (see `requirements.txt`).
No pytest; `tests/test_stage1.py` runs standalone (`python3 tests/test_stage1.py`).
