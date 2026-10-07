# Literature Review — Grounding Research for the NTN Paper Revision

**Paper (working retitle):** "From Illustrative to Measured: Task-Oriented Semantic mIoT over NTN for Remote Agriculture and Environmental Sensing"
**Target venue:** SPACOMM 2027 (IARIA, 19th Int. Conf. on Advances in Satellite and Space Communications), Lisbon, April 18–22, 2027. Full-paper deadline: **Dec 28, 2026**.
**Revision scope:** narrow to two applications (smart agriculture — irrigation decisions; environmental monitoring — flood warnings; India-oriented lens); replace "Required Results" (old Sec. V.B) with real trace-driven simulation results from the paper's three-stage protocol.
**Compiled:** 2026-10-01. Detail files: `track1-ntn-deployments.md`, `track2-semantic-lit.md`, `track3-datasets.md`, `track4-critiques.md` (same directory).

## Verification notes

Key facts were independently re-verified by the synthesizer (2026-10-01); corrections to the track files are flagged below. Rule followed throughout: no invented values, dates, or URLs.

- **Mannoni et al., VTC2022-Spring** — confirmed real: IEEE VTC2022-Spring, Helsinki, Jun 2022, DOI `10.1109/VTC2022-Spring54318.2022.9860902`; open-access PDF via HAL `cea-04564460`. This is the anchor peer-reviewed system simulation for NB-IoT NTN parameters.
- **Richter 2026 thesis** — confirmed real: Dominic Richter, bachelor thesis 2026, "Practical Performance Analysis of NB-IoT across Terrestrial and Non-Terrestrial Networks" (field measurements with COTS modem over commercial GEO NB-NTN). **Caveat:** it is a *bachelor thesis*, not peer-reviewed — cite as field-measurement evidence with that label, and prefer Mannoni et al. wherever both give a number.
- **Zenodo 19707421** (East Kazakhstan agromet) — verified live; published 2026-04-23, CC-BY-4.0, 15.1 MB download present.
- **Zenodo 15349031** (GRDC-Caravan) — verified live; **correction:** published **2025-05-06** (track 3 wrote 2026-05-06), CC-BY-4.0, 5356 catchments / 25 countries / 1950–2023.
- **DOIs verified via Crossref** (title/venue/year all match): DELTA `10.1109/INFOCOM55648.2025.11044748`; Wiangnak `10.3390/s26113512`; Peng `10.1109/mnet.2024.3380817`; TinyHAR-UQ `10.1016/j.iot.2026.101889`; X. Chen `10.1109/lwc.2025.3569205`; Górecki `10.3390/electronics15174000`; Nguyen ComST `10.1109/comst.2025.3616973`; Jiang JSAC `10.1109/jsac.2025.3559113`; Air-ODE `10.1109/TCCN.2025.3569604` (Crossref year 2026 — early access 2025; cite as early-access/2026).
- **DELTA title discrepancy resolved:** arXiv:2412.07503 confirms the conference title "Goal-Oriented Medium Access with Distributed Belief Processing" (INFOCOM 2025). The Crossref DOI record shows the *journal-version* title "Distributed Optimization of Age of Incorrect Information with Dynamic Epistemic…" (IEEE Trans. Networking). Cite with the conference title + DOI; mention the journal version if needed.

---

## (a) Annotated bibliography

Priority marks: **[MUST]** = cite in the revision; **[REC]** = recommended; **[BG]** = background if space allows. All arXiv-only entries are labeled.

### A. NTN measurements, standards, and link-budget grounding (supports Sec. IV models, Sec. VII simulation)

**[MUST] 1.** V. Mannoni, V. Berg, S. Cazalens, and P. Raveneau, "System Level Evaluation for NB-IoT Satellite Communications," *Proc. IEEE VTC2022-Spring*, Helsinki, Jun. 2022, pp. 1–6. DOI: 10.1109/VTC2022-Spring54318.2022.9860902. Open access: https://cea.hal.science/cea-04564460
CEA/CNES system-level simulation of NB-IoT over LEO (770 km) and GEO: LEO single-carrier uplink 1.28 kb/s at 23 dBm; ~5 s end-to-end for a 300 B message at low load rising to ~25 s at 600+ users/spot; 660–890 supported users per spot; per-spot visibility only 45 s–3.5 min, so a device may not finish one attach+data transaction per spot pass (NB-IoT has no handover).
→ **Supports Sec. IV-B/IV-D/IV-G and Sec. VII-B:** the primary peer-reviewed source for defensible T_RA, K, R, and per-spot capacity numbers; also the source of the "discontinuous visibility" correction to the paper's beam model.

**[MUST] 2.** D. Richter, "Practical Performance Analysis of NB-IoT across Terrestrial and Non-Terrestrial Networks," bachelor thesis, 2026. PDF: https://theinternetofthings.eu/wp-content/uploads/2026/03/Bachelor-Thesis-2.-Practical-Performance-Analysis-of-NB-IoT-across-Terrestrial-and-Non-Terrestrial-Networkspdf.pdf
Field measurements with a COTS NB-IoT modem over a commercial GEO NB-NTN link (Leipzig): mean attach 93.3 s costing 6,656 mAs (~1.85 mAh); 200 B payload median latency 13.4–34.9 s depending on antenna; NTN payload TX energy 150–420× optimal terrestrial (13–38× edge-of-cell); TCP incurred 147% protocol overhead with frequent timeouts while CoAP/UDP was reliable.
→ **Supports Sec. IV-E (energy model) and Sec. VII:** the only found *measured* (not simulated) NTN-IoT energy/latency numbers — anchors E_access and E_tx; label as thesis field measurements, not peer-reviewed.

**[REC] 3.** 3GPP TR 36.763, "Study on NB-IoT/eMTC support for NTN," Rel-17, 2021 (already cited as [1] in the draft).
Keep as the standards anchor; add that Rel-17/18 specify bent-pipe NB-IoT NTN (GNSS pre-compensation, HARQ disabled, blind repetitions) while Rel-19's store-and-forward/regenerative operation (IoT_NTN_Ph3, RP-234077) is specified but **not yet deployed** — so the paper's sparse-LEO scenario should be framed as standards-track, not commercial reality.

**[BG] 4.** R. Sørensen et al., "NB-IoT for NTN LEO," *Proc. Small Satellite Conf.*, 2021. arXiv:2108.06172. https://arxiv.org/abs/2108.06172
States the standard NB-IoT power class 3 (23 dBm / 200 mW) used throughout NTN link budgets.
→ **Supports Sec. IV:** one-line citation for the 23 dBm device assumption.

### B. Semantic / task-oriented / goal-oriented MAC and NTN (supports Sec. II positioning, Sec. III, Sec. IV-G, Sec. VII-B)

**[MUST] 5.** F. Chiariotti, A. Munari, L. Badia, and P. Popovski, "Goal-Oriented Medium Access with Distributed Belief Processing," *Proc. IEEE INFOCOM 2025*. DOI: 10.1109/INFOCOM55648.2025.11044748. arXiv:2412.07503. (Journal version in *IEEE Trans. Networking* under the title "Distributed Optimization of Age of Incorrect Information with Dynamic Epistemic…".)
The DELTA protocol: devices report only anomalies using distributed belief about Age of Incorrect Information; Monte-Carlo results show ≥30% improvement over classical random access and state-of-the-art scheduled schemes in large networks, robust to imperfect feedback.
→ **Supports Sec. IV-G / VII-B:** a realistic, simulation-evaluated goal-oriented MAC to reference (and approximate) instead of a stylized collision model; its anomaly-triggered uplink maps directly onto the paper's admission-control claim.

**[REC] 6.** P. Talli, A. Munari, F. Mason, F. Chiariotti, and A. Zanella, "Value-Based Massive Access through Goal-Oriented Irregular Repetition Slotted ALOHA," arXiv:2609.20569 [cs.NI], Sep. 2026. **[arXiv-only]** https://arxiv.org/abs/2609.20569
Push-based goal-oriented IRSA: the base station broadcasts a Value-of-Information threshold and devices transmit only above it; on a 2,000-node Wiener-process model it cuts average and worst-case estimation error by >30% versus optimal centralized policies.
→ **Supports Sec. IV-G / VII-B:** a massive-access-flavored goal-oriented MAC (2,000 nodes); note 3GPP Rel-19 NB-IoT embraces IRSA, which connects it to the NTN context.

**[REC] 7.** P. Agheli, N. Pappas, and M. Kountouris, "Semantic Filtering and Source Coding in Distributed Wireless Monitoring Systems," *IEEE Trans. Commun.*, vol. 72, no. 6, pp. 3290–3304, Jun. 2024. https://arxiv.org/abs/2305.11549
Formulates goal-dependent packet admission/drop at the source with truncated error control and derives optimal codeword lengths maximizing a weighted semantic-utility objective; improves timely delivery of important updates under a rate constraint.
→ **Supports Sec. III and VII-C:** a clean peer-reviewed formulation of "which packets deserve airtime" to motivate the admission-control rule.

**[MUST] 8.** H. Peng, Z. Zhang, Y. Liu, Z. Su, T. H. Luan, and N. Cheng, "Semantic Communication in Non-Terrestrial Networks: A Future-Ready Paradigm," *IEEE Network*, vol. 38, no. 4, pp. 119–127, Jul. 2024. DOI: 10.1109/mnet.2024.3380817
Proposes an SC-based NTN architecture (AI-driven semantic extraction + physical-layer security + semantic-aware resource management) and reports experiments showing improved coverage efficiency and robustness in satellite–UAV–ground scenarios versus conventional communication.
→ **Supports Sec. II:** peer-reviewed, ComSoc best-readings-listed evidence that semantic NTN is moving from vision to tested architecture — updates the related work beyond Minani et al. [10][11].

**[REC] 9.** P. Jiang, C.-K. Wen, X. Li, S. Jin, and G. Y. Li, "Semantic Satellite Communications Based on Generative Foundation Model," *IEEE J. Sel. Areas Commun.*, vol. 43, no. 7, pp. 2431–2445, Jul. 2025. DOI: 10.1109/jsac.2025.3559113
Builds a satellite SemCom system on a generative foundation model that reconstructs semantically rich content from very few transmitted features.
→ **Supports Sec. III:** peer-reviewed proof that generative receiver-side reconstruction can substitute for raw-payload transmission — cite cautiously as the paper's most aggressive bandwidth-saving precedent.

**[REC] 10.** W. Chen, S. Li, C. Ju, D. Wang, J. Li, and D. Wang, "Semantic-Enhanced Downlink LEO Satellite Communication System With OTFS Modulation," *IEEE Commun. Lett.*, vol. 28, no. 6, pp. 1377–1381, Jun. 2024. DOI: 10.1109/lcomm.2024.3386748
Semantic enhancement on a downlink LEO system using OTFS modulation (suited to high-Doppler LEO channels).
→ **Supports Sec. IV-B:** waveform-level evidence that semantic coding is compatible with LEO-friendly modulation.

**[BG] 11.** G. Zheng, Q. Ni, K. Navaie, and H. Pervaiz, "Semantic Communication in Satellite-Borne Edge Cloud Network for Computation Offloading," *IEEE J. Sel. Areas Commun.*, vol. 42, no. 5, pp. 1145–1158, May 2024. DOI: 10.1109/jsac.2024.3365879
Jointly optimizes semantic extraction versus computation offloading aboard satellites (edge cloud).
→ **Extends Sec. IV-E / VI-F:** the compute-vs-radio trade-off implemented satellite-side — a useful contrast to the paper's device-side framing.

**[MUST] 12.** L. X. Nguyen et al., "A Contemporary Survey on Semantic Communications: Theory of Mind, Generative AI, and Deep Joint Source-Channel Coding," *IEEE Commun. Surveys & Tutorials*, vol. 28, 2026. DOI: 10.1109/comst.2025.3616973
2026 survey covering Theory-of-Mind SemCom, generative-AI SemCom, and deep JSCC.
→ **Supports Sec. II:** the up-to-date survey anchor so the paper positions itself once against a 2026 baseline rather than 2021–2023 surveys.

### C. Inference-energy vs. radio-savings trade-off (supports Sec. IV-E, Sec. VI-F, Sec. VII-D)

**[MUST] 13.** X. Chen, C. Huang, G. Chen, D. Feng, and P. Xiao, "The Communication and Computation Trade-Off in Wireless Semantic Communications," *IEEE Wireless Commun. Lett.*, vol. 14, no. 7, pp. 2259–2263, Jul. 2025. DOI: 10.1109/lwc.2025.3569205
Analyzes where the compute-vs-transmit optimum lies for wireless semantic communications — when local semantic inference earns back more radio energy than it costs.
→ **Directly supports Sec. IV-E / VI-F:** independent peer-reviewed corroboration of the paper's break-even argument.

**[MUST] 14.** S. Górecki, S. Hausman, and P. Korbel, "Cross-Layer Energy Management in Embedded AIoT Sensor Networks: A Structured Review, Full-Cycle Energy Model, and Break-Even Analysis," *Electronics*, vol. 15, no. 17, Art. 4000, 2026. DOI: 10.3390/electronics15174000
Structured review (548 records screened) plus full-cycle energy model and break-even analysis for on-device AI; coins "semantic compression" for replacing raw measurements with inferred descriptors and states its energy benefit is *not automatic*; an LTE-M experiment (40 transactions) shows payload length alone cannot characterize communication energy — fixed overhead dominates short packets (state-aware model R² = 0.980).
→ **Supports Sec. IV-E and the fixed-overhead H argument (VI-B/C):** peer-reviewed empirical backing that per-packet overhead dominates short-packet energy — the regime where the paper's argument is strongest; also warrants the sensitivity sweep over H.

**[MUST] 15.** I. Lamaakal et al., "TinyHAR-UQ: Battery-aware, uncertainty-controlled tinyML for wearable activity recognition on IoT edge devices," *Internet of Things*, vol. 36, Art. 101889, Mar. 2026. DOI: 10.1016/j.iot.2026.101889
Int8 TinyML with early exits on nRF52840 (Cortex-M4F) and ESP32-S3: 92.4–93.2% accuracy, 3–6 ms latency, **0.54–0.92 mJ per inference**, 48–54 KB RAM.
→ **Supports Sec. IV-E:** the concrete per-inference energy anchor for the break-even calculation (note: activity recognition, so it *bounds* rather than equals a semantic encoder's cost; no published measurement exists of a semantic encoder on MCU-class hardware over an NTN link — state this openly).

### D. Application evidence — irrigation decisions and flood warnings (supports Sec. V-D, V-E)

**[MUST] 16.** K. Taueatsoala et al., "TinyML-Enabled IoT for Sustainable Precision Irrigation," arXiv:2601.13054 [cs.LG], Jan. 2026. **[arXiv-only]** https://arxiv.org/abs/2601.13054
Edge-first irrigation: ESP32 TinyML node + Raspberry Pi edge server, soil-moisture/temperature/humidity/pH/light sensors; on-device model predicts irrigation needs with MAPE < 1%; fully offline-capable; controlled-environment validation cut water use versus traditional methods.
→ **Supports Sec. V-D:** 2026 demonstration that the *decision* (irrigate / don't irrigate) can be made on-device with ~1% error — the exact "transmit the decision, not the data" traffic pattern the semantic scheme assumes. Flag: controlled-environment validation, not field-scale.

**[REC] 17.** E. Artetxe et al., "Smart IoT Irrigation System Based on Fuzzy Logic, LoRa, and Cloud Integration," *Electronics*, vol. 13, no. 10, Art. 1949, May 2024. DOI: 10.3390/electronics13101949
LoRa-linked fuzzy-logic irrigation with weather-forecast input, hardware-in-the-loop validated: 23.1% water-loss reduction versus on/off control over four days (+4.07% with forecast).
→ **Supports Sec. V-D:** peer-reviewed, hardware-in-the-loop quantification of decision-driven irrigation savings — an independent non-semantic baseline the simulation can aim to beat.

**[MUST] 18.** V. Wiangnak, M. Wiboonrat, and S. Duangsuwan, "Development of an AIoT-Based Early Flash-Flood Warning System for Smart Rural Disaster Resilience," *Sensors*, vol. 26, no. 11, Art. 3512, Jun. 2026. DOI: 10.3390/s26113512
YOLOv10 water-level detection + LSTM forecaster in a **60-day field deployment** at two rural Thailand sites: detection probability > 0.92, critical success index > 0.82, 4–5 s end-to-end warning latency, >97% uptime.
→ **Supports Sec. V-E:** a peer-reviewed field-deployed performance bar for flood warnings. **State the limitation:** it uses 5G/CCTV, not LPWAN/NTN — the paper's contribution is approaching that bar under NTN link budgets, not matching the setup.

### E. Critiques, limitations, and honest-framing sources (supports Sec. II, Sec. IX bounded language)

**[MUST] 19.** D. Gündüz et al., "Beyond Transmitting Bits: Context, Semantics, and Task-Oriented Communications," *IEEE J. Sel. Areas Commun.*, vol. 41, no. 1, pp. 5–41, Jan. 2023. DOI: 10.1109/JSAC.2022.3223408
Treats semantics operationally as a generic distortion measure — semantic communication is generalized rate–distortion, not a new physical-layer regime; task-tied gains generalize poorly across scenarios ("a tradeoff between optimization and generalization needs to be explored").
→ **Supports Sec. II.B / IX:** the field's flagship paper itself says task-tied gains don't generalize — cite it to present the paper's bounded framing as consensus, not timidity.

**[MUST] 20.** G. Xin, P. Fan, and K. B. Letaief, "Semantic Communication: A Survey of Its Theoretical Development," *Entropy*, vol. 26, no. 2, Art. 102, 2024. DOI: 10.3390/e26020102
Semantic channel capacity can be higher *or lower* than physical capacity depending on semantic ambiguity and KB quality; "rate > Shannon C" claims hold only when nonzero BER is tolerated while semantic error stays zero — i.e., the limit is "broken" by *changing the success criterion*.
→ **Supports Sec. II.B / VI.G / IX:** the definitive rebuttal of "break Shannon's limit" phrasing; never let "semantic capacity" or "capacity gain" appear in the revision.

**[REC] 21.** N. Tavakolian, H. Purmehdi, and J. Baek, "Rethinking Communication Metrics: How Should We Measure Meaning?" arXiv:2608.21626, Aug. 2026. **[arXiv-only]** https://arxiv.org/abs/2608.21626
Evaluation-centered survey: no single metric characterizes semantic quality across tasks and channels; published percentages use mutually incomparable metrics/baselines; semantic drift occurs when KBs evolve independently.
→ **Supports Sec. II.A and IX:** backs the disclaimer that the cited 50%/73%/87.5%/4× figures "are not reproduced or combined here" — add one clause citing metric-incomparability; also backs the fixed-operating-point comparison design (V.A).

**[REC] 22.** L. A. Lastras et al., "Breaking through the classical Shannon entropy limit: A new frontier through logical semantics," arXiv:2501.00612, Dec. 2024. **[arXiv-only]** https://arxiv.org/abs/2501.00612
Shannon-style analysis (IBM/Purdue) showing semantic efficiency gains arise from *shared receiver reasoning and knowledge*, not the channel — gains evaporate under KB mismatch.
→ **Supports Sec. II.B / VI.G:** attribute the gain decomposition explicitly (1/q = admission logic; payload factor = shared-model compression) and note both depend on a shared KB.

**[REC] 23.** Language-mismatch study, *Proc. IEEE ISWCS 2024* (arXiv:2405.20085). https://export.arxiv.org/pdf/2405.20085
When transmitter and receiver semantic models are not jointly trained, mismatch arises *even with identical architectures, data, and objectives* → confident misinterpretation; compensation needs extra signaling (KB management has a communication cost).
→ **Supports Sec. III.B/C and VII.C:** motivates the model-identifier/fallback design and the *undetected*-drift experiments.

**[REC] 24.** K. J. Åström and B. Bernhardsson, "Comparison of Riemann and Lebesgue sampling for first order stochastic systems," *Proc. IEEE CDC*, 2002 (and the event-triggered control literature, e.g., *Sensors* 2018 review https://www.mdpi.com/1424-8220/18/8/2547).
Event-triggered (Lebesgue) sampling — transmitting only on significant change — predates "semantic communication" by decades and is a measured, real gain that is *not* attributable to semantics or AI.
→ **Supports Sec. II.B / V.A / VII.C:** warrants making the event-triggering/compression ablations **mandatory** ("shall be included"), not conditional; credit report suppression honestly as event-triggered admission.

**[REC] 25.** R. Meng et al., "A Survey of Secure Semantic Communications," arXiv:2501.00842, Jan. 2025. **[arXiv-only]** http://arXiv.org/abs/2501.00842
Threats across the SemCom lifecycle (model inversion, adversarial/backdoor attacks, privacy inference on semantic features); a transmitted semantic label/decision can itself be the sensitive asset — link-layer confidentiality does not imply semantic privacy.
→ **Supports Sec. VIII.B:** keep "Confidentiality of raw data does not guarantee semantic privacy" and cite this; add spoofed-metadata/model-poisoning cases to the evaluation requirements.

---

## (b) Defensible NTN link/energy parameter table (for the simulation)

Confidence labels: **[M]** measured (field/hardware) · **[S]** specified (3GPP) · **[SIM]** peer-reviewed system/link simulation · **[E]** estimated from geometry (method shown). Gaps are stated explicitly at the end.

| # | Parameter | Defensible value / range | Source (where the number appears) | Conf. |
|---|---|---|---|---|
| 1 | NB-IoT NTN uplink rate, LEO, 23 dBm | **1.28 kb/s** single-carrier (3.75 kHz); 8.2 kb/s with 3 subcarriers | Mannoni et al., VTC2022-Spring, Table III | SIM |
| 2 | NB-IoT NTN uplink rate, GEO, 23 dBm | **80 b/s** single-carrier | Mannoni et al., Table III | SIM |
| 3 | NPRACH / NPUSCH repetitions | NPRACH 1 (LEO) / 8 (GEO); NPUSCH up to **128** max (DCI Format N0); HARQ disabled on NTN | Mannoni et al., Table III & §II-B; 3GPP Rel-17 NTN | SIM/S |
| 4 | Access + setup time T_RA, LEO (low load) | Sync 2560 ms + RA ~400 ms + security/attach/auth + data ~2025 ms → **~5 s end-to-end** for 300 B @23 dBm; ~25 s at 600+ users/spot | Mannoni et al., §III-C, Fig. 6 | SIM |
| 5 | End-to-end latency, GEO (low load) | **66 s** @23 dBm (24 s @27 dBm; 19 s @30 dBm); network sync + RA alone 8.9 s | Mannoni et al., §III-C, Fig. 7 | SIM |
| 6 | **Measured** GEO NB-NTN attach | **93.3 s mean**, 6,656 mAs (~1.85 mAh), RSRP −120…−126 dBm | Richter 2026 thesis, §4.3.1 Table 5 | M |
| 7 | **Measured** GEO NB-NTN payload latency | 200 B: median **34.9 s** (linear antenna) → **13.4 s** (directive circular-polarized) | Richter 2026 thesis, §4.4 | M |
| 8 | **Measured** message drop rate, GEO | 9.0% (linear) → ~1.1% (circular antenna) | Richter 2026 thesis, §4.4 | M |
| 9 | Protocol overhead per message | TCP over GEO NTN: **147% overhead**, frequent timeouts; CoAP/UDP reliable, no loss observed; a 300 B UE message sent as 8 NPUSCH packets of 328 bits | Richter thesis §4.2.1; Mannoni et al., Table II | M/SIM |
| 10 | Device TX power | **23 dBm (200 mW)** power class 3 (highest standard NB-IoT class) | Sørensen et al. 2021; 3GPP | S |
| 11 | **Measured** NTN energy per attach | **6,656 mAs mean (~1.85 mAh)** | Richter 2026 thesis, §4.3.1 | M |
| 12 | **Measured** NTN energy per payload | 150 B: 4,843 mAs (33.8 s active); 250 B: 9,083 mAs (59.9 s); mean draw **155–168 mA** at max TX power | Richter 2026 thesis, §4.3.2 Table 6 | M |
| 13 | NTN energy multipliers vs terrestrial | Payload TX: **150× (150 B) to 400–420× (250–750 B)** vs optimal TN; **13× to 30–38×** vs edge-of-cell TN | Richter 2026 thesis, §4.3.4 | M |
| 14 | LEO RTT, ~600 km | **4.0 ms** (zenith) – **12.9 ms** (10° elevation, 1,932 km slant) | Circular-orbit geometry (R=6,371 km) | E |
| 15 | LEO pass duration, 600 km, fixed point | **12.8 min** max horizon-to-horizon; **~8.5 min** above 10° elevation | Geometry; consistent w/ Cakaj (5–15 min, 6–8×/day) | E |
| 16 | Per-spot (beam) visibility, LEO | **45 s (central) – 3.5 min (peripheral)**; <1 min for 50% of cases — a device may *not* finish one attach+data transaction per spot pass (no NB-IoT handover) | Mannoni et al., §II-A, Fig. 2 | SIM |
| 17 | Supported users per spot (300 B, 30 msg/day) | LEO: **660 (23 dBm)** → 890 (27/30 dBm); GEO: 115 → 3,000 | Mannoni et al., §III-C, Fig. 8 | SIM |
| 18 | MCU inference energy anchor | **0.54–0.92 mJ/inference** (int8 TinyML, Cortex-M4F nRF52840); 3–6 ms latency | TinyHAR-UQ, *Internet of Things* 2026 | M |
| 19 | NB-IoT air interface basics | 180 kHz carrier; UL single-tone 3.75 kHz; max coupling loss ~164 dB | 3GPP Rel-13 design targets | S |

**Numbers explicitly unavailable (do not invent; model as sensitivity ranges):** live-network NPRACH collision rates / RA success on commercial NTN (undisclosed); repetition factors actually configured by Skylo/Sateliot/OQ (not disclosed); per-message byte overhead of a Rel-17 NTN attach on a live network (unmeasured); device-side inference energy for a *semantic encoder* on an NTN chipset (no published measurements — the paper's Sec. VII-D rule applies: present as sensitivity ranges, not hardware claims).

**Key modeling implication (verified against measurements):** access/setup dominates tiny payloads — LEO ~5 s setup vs sub-second-to-seconds of payload airtime; measured GEO attach ≈ 1.85 mAh ≈ the energy of hundreds of payload bytes. The gain mechanism is therefore overwhelmingly **report suppression (N_x), not payload shrinking (L_x)** — the simulation and the paper should say so explicitly and credit suppression first. E_access must be a first-class term in Eq. (5); E_retx should be reframed as blind-repetition overhead K plus RLC-ARQ residual (HARQ is disabled on NTN).

---

## (c) Recommended real datasets (all download links verified 2026-10-01)

### Agriculture (for V.D — irrigation decisions)

**1. USDA NRCS SCAN — Soil Climate Analysis Network** (primary sensor trace)
- Hourly soil moisture + soil temperature (multiple depths), air temp, relative humidity, precipitation, solar radiation; 200+ US ag sites; multi-decadal.
- Fully open, no registration, public domain. https://www.wcc.nrcs.usda.gov/scan/
- *Use:* the four V.D sensing channels at hourly cadence; define the irrigation task (soil-moisture deficit + trailing-48h rain ⇒ irrigate/defer/inspect). Caveats: US-only (pair with IMD for the India lens); hourly granularity; drop long station-outage gaps from task scoring, don't impute.

**2. ISMN — International Soil Moisture Network** (India validation holdout)
- Global network-of-networks incl. the **IITM (Indian Institute of Tropical Meteorology) network** — the closest openly downloadable in-situ Indian soil-moisture trace. Free registration required. https://ismn.earth/en/data/data-download/
- *Redistribution caveat:* ISMN terms forbid re-export — the reproducibility package must ship scripts + trace IDs, not data files. Sparse Indian coverage: use as holdout, train on denser networks.

**3. IMD gridded daily rainfall (0.25°) + tmin/tmax (1.0°)** (India-lens forcing/regime labels)
- Open, no registration, 1901–present. Rainfall: https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_Bin.html ; temperature: https://imdpune.gov.in/cmpg/Griddata/Max_1_Bin.html and https://imdpune.gov.in/cmpg/Griddata/Min_1_Bin.html ; Python access via MIT-licensed `imdlib`: https://github.com/iamsaswata/imdlib
- *Use:* drive the event schedule and stratify results into dry / normal / heavy-rain / monsoon (as V.D requires). It is a regime label and event driver, **not** an IoT trace — never use as the sensor channel.

**4. East Kazakhstan agrometeorological network, 2022–2025** (secondary robustness trace)
- Hourly + minute-resolution multi-variable field data (temp, humidity, precip, soil temp/moisture to 100 cm), 3 stations, 4 growing seasons, CC-BY-4.0, 15.1 MB. https://zenodo.org/records/19707421
- *Use:* robustness check of the irrigation-decision logic on a second real trace (not the India headline).

### Environmental monitoring (for V.E — flood warnings)

**5. GRDC-Caravan extension** (long-record discharge for event statistics)
- Daily river discharge 1950–2023, 5356 catchments / 25 countries + ERA5-Land forcing + 211 catchment attributes, CC-BY-4.0. https://zenodo.org/records/15349031
- *Use:* flood-warning event definition (discharge percentile exceedance), false-alarm rates over decades, correlated monsoon bursts. **Check before claiming India coverage:** India is not confirmed in the 25-country set — if absent, position as methodology validation and use IMD rainfall as the India event driver. Daily resolution misses flash peaks — pair with #6.

**6. USGS NWIS Water Services** (sub-daily water level for burst analysis)
- ~15-min gage height (water level, parameter 00065) + discharge (00060) via open REST APIs, no key, US public domain. https://waterservices.usgs.gov/
- *Use:* the sub-daily dynamics and geographically correlated burst analysis V.E mandates (synchronize nearby gauges across a shared storm window). Caveats: US-only; recent 15-min data are provisional; sensor dropouts during flood peaks are missed-detection contributors — report, don't interpolate.

### Do not waste time on (verified inaccessible)
India-WRIS/CWC gauge data (portal times out; institutional registration; border-basin data classified); classic GRDC portal (request-only, no redistribution); IMD station-level point data (paid); DEEP FARM banana IoT dataset (Zenodo files restricted); Kaggle "IoT smart farm" CSVs (frequently synthetic, unverifiable provenance); IMD AWS/ARG API (institutional credentials only).

---

## (d) Claims in the current draft to soften or cut

Section references are to the draft at `/tmp/ntn_paper.txt`. Most are rewordings, not cuts — the draft is already unusually careful (II.B, VI, IX), and the items below are residual vulnerabilities with published warrants from §(a)E.

1. **II, related-work percentages (50% / 73% / 87.5% / 4×).** The draft already says these "are not reproduced or combined here" (II.A) — keep it and add one clause citing Tavakolian et al. [21]: *"published percentages use mutually incomparable metrics and baselines, so they are cited as directional evidence only."*
2. **VI.E, the 32.5× illustrative calculation.** Well bounded in the text, but a large ratio in the body *will* be quoted out of context. Append: *"This ratio is a teaching example, not a finding; measured results are reported per Section VII with the attributions of Section II.B."*
3. **II.B / V.A / VII.C: event triggering and compression as reference mechanisms "where relevant" / "may be included."** This is the soft spot the Åström/event-triggered literature [24] attacks. Change to mandatory: *"The ablation always includes deterministic event triggering and conventional compression baselines, so that any residual gain is attributable to the semantic/task-oriented mechanism rather than to ordinary compression or report suppression."*
4. **V.C application hypotheses.** Correctly phrased as hypotheses; guard them with the Gündüz et al. [19] caveat: *"These hypotheses are application-specific and non-transferable across the five classes."* Never let them harden into claimed results in the conclusion.
5. **III.A/III.D, "self-evolving" / "self-evolution."** The mechanism described is guarded closed-loop adaptation with validated redeployment — rename to **"controlled adaptation (two time scales)"** and keep the guardrail sentences verbatim. The hype-adjacent label invites misreading as unconstrained online learning.
6. **III.A, "assigns confidence and urgency."** Assumes calibrated on-device confidence. Add one sentence (III.B or VII.C): *"Confidence values must be calibration-validated on the deployment distribution; uncalibrated confidence is treated as a fault input, triggering conservative fallback."* (Warrant: [21], [23].)
7. **V.I population arithmetic (96M reports/day etc.).** Already labeled "offered-traffic calculations, not claims of supported beam capacity" — keep the label and the "methodological stress range" phrasing for the 10³–10⁶ sweep.
8. **VIII.B metadata security.** "May require integrity and replay defense" undersells the broadcast-NTN threat ([25] and the agentic-eavesdropping work): reword to *"requires integrity and replay protection, because forged urgency/confidence can exhaust shared beam resources; evaluation includes spoofed-metadata and model-poisoning cases."*
9. **Cut candidate: any sentence implying semantic reporting is inherently more private/secure than raw reporting.** The draft does not currently make this claim — verify it stays that way ([25] argues the opposite is often true).
10. **X conclusion metric list.** Fine as a checklist, but every reported gain (especially task-throughput efficiency and supported devices per beam) must carry its **bounded-language attachment**: named application, dataset, task constraint, energy model, access configuration, load range — never bare percentages (warrant: [19], [20], [21]).

---

## Honest-evaluation checklist for the revision's simulation

1. **Fix the task operating point first** (accuracy, missed-event probability, deadline); measure everything at that common point per scheme (V.A; [19], [21]).
2. **Mandatory two-mechanism ablation**: payload coding vs. admission/suppression vs. scheduling metadata vs. retraining traffic, with deterministic event triggering and conventional compression always baselined (VII.C; [22], [24]).
3. **Strong conventional baselines, same trace and channel realization** — no strawmen (V.A, VII.A; [24]).
4. **Uncertainty quantification**: seeds, mean/median, confidence intervals; rare-event misses need adequate event counts or report a bound (VII.D; [21]).
5. **Full-cycle energy as sensitivity ranges**, including model-update distribution energy; sweep fixed overhead H and inference energy explicitly — break-even is bounded by per-message overhead (IV.E, VII.D; [14]).
6. **KB-mismatch and undetected-drift runs** with fallback exercised under *silent* degradation (III.B/C, VII.C; [23]).
7. **Adversarial/privacy evaluation of the semantic layer**: forged urgency/confidence, model poisoning, semantic-label leakage under encryption (VIII.B; [25]).
8. **Stratified claims only** — per application, dataset, constraint, energy model, access config, and load regime (incl. correlated bursts and near-saturation with widened CIs); permitted term is *resource-utilization/task-outcome gain*, never "capacity gain" or "beyond Shannon" ([19], [20], [21]).

---

## Open gap the revision fills (honest positioning statement)

Across all four research tracks, **no 2024–2026 publication was found that measures a semantic/task-oriented encoder running on MCU-class hardware over a real NTN or LPWAN link**. The closest evidence is simulation (DELTA, GO-IRSA, Air-ODE, Agheli), edge-class hardware (MambaJSCC on Jetson AGX Orin), MCU-class inference on a non-semantic task (TinyHAR-UQ, 0.54–0.92 mJ), or field AIoT on non-NTN links (Wiangnak flood warning on 5G/CCTV). The revision's trace-driven simulation — real sensor traces (SCAN/ISMN/IMD, GRDC-Caravan/USGS) through a measurement-anchored NTN link/energy model (Mannoni/Richter parameters) — should be framed explicitly as narrowing this gap, with bounded claims per the checklist above.
