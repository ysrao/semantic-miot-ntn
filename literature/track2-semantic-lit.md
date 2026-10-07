# Track 2 — Semantic / Goal-Oriented / Task-Oriented Communication Literature (2024–2026)

Literature research for the revision of *"Application-Specific Semantic and Task-Oriented Communication for Massive IoT over NTN."*
Compiled 2026-10-01. Covers semantic, task-oriented, and goal-oriented communication work from 2024–2026 that is **not already cited** in the paper's reference list [1]–[12]. Papers [4]–[11] (Strinati & Barbarossa 2021; Getu et al. 2023; Delfani & Pappas 2025; Delfani et al. 2026; Zeydan et al. 2025; Uysal & Li 2024; Minani et al. 2024/2025) are **not re-reported** except where a newer follow-up is noted.
Peer-reviewed venues are preferred; arXiv-only papers are **clearly labeled**. All venues/years were verified against Crossref, IEEE, MDPI, or the arXiv record — nothing is invented. All URLs are copied verbatim from the sources they were found on.

---

## A. Goal-oriented medium access — realistic MAC models beyond [9]

### 1. F. Chiariotti, A. Munari, L. Badia, and P. Popovski, "Goal-Oriented Medium Access with Distributed Belief Processing," *Proc. IEEE INFOCOM 2025*, London, UK, 2025. DOI: 10.1109/INFOCOM55648.2025.11044748. Journal version: *IEEE Trans. Networking* (accepted 2 Nov 2025, current version 5 Jan 2026). arXiv:2412.07503. https://arxiv.org/abs/2412.07503

The DELTA protocol uses distributed belief processing so that devices report only anomalies rather than raw readings, minimizing the Age of Incorrect Information at the receiver. Monte-Carlo simulations show DELTA beats classical random access and even state-of-the-art scheduled schemes by ≥30% in large networks, and retains its advantage under imperfect feedback.
→ **Supports/extents Sec. IV-G and Sec. VII-B:** gives a realistic, simulation-evaluated goal-oriented MAC to replace the stylized collision model — cites exactly what DELTA was measured to do (≥30% improvement, anomaly-triggered uplink).

### 2. P. Talli, A. Munari, F. Mason, F. Chiariotti, and A. Zanella, "Value-Based Massive Access through Goal-Oriented Irregular Repetition Slotted ALOHA," arXiv:2609.20569 [cs.NI], Sep. 2026. **[arXiv-only]** https://arxiv.org/abs/2609.20569

Push-based goal-oriented variant of IRSA (irregular repetition slotted ALOHA): the base station broadcasts a Value-of-Information (VoI) threshold and devices transmit only when their measurement exceeds it. On a distributed Wiener-process model with 2,000 nodes, it cuts average and worst-case estimation error by more than 30% versus optimal centralized policies, and stays robust to imperfect successive interference cancellation.
→ **Supports Sec. IV-G / Sec. VII-B:** a second, more massive-access-flavored goal-oriented MAC (2,000 nodes) whose VoI-threshold mechanism maps directly onto the paper's "transmit only when semantically significant" claim; note the paper itself observes IRSA is embraced in 3GPP Rel-19 NB-IoT.

### 3. P. Agheli, N. Pappas, and M. Kountouris, "Semantic Filtering and Source Coding in Distributed Wireless Monitoring Systems," *IEEE Trans. Commun.*, vol. 72, no. 6, pp. 3290–3304, Jun. 2024. arXiv:2305.11549. https://arxiv.org/abs/2305.11549

Formulates goal-dependent packet admission/drop at the source plus truncated error control, and derives optimal codeword lengths that maximize a weighted semantic-utility objective; analytical and numerical results show it improves timely delivery of the *important* updates under a rate constraint.
→ **Supports Sec. III (semantic encoder design) and Sec. VII-C:** a clean, peer-reviewed formulation of "which packets deserve airtime" — directly usable to motivate the admission-control rule in the proposed 3-stage protocol.

---

## B. Semantic communication specifically over NTN — positioning beyond [10][11]

### 4. L. X. Nguyen, A. D. Raha, P. S. Aung, D. Niyato, Z. Han, and C. S. Hong, "A Comprehensive Survey on Semantic Communication in Non-Terrestrial Networks: Architectures, Methodologies, and Challenges," arXiv:2606.05216, Jun. 2026. **[arXiv-only]** https://arxiv.org/abs/2606.05216

Maps each NTN limitation (delay, bandwidth, intermittent connectivity, energy) to the SemCom property that addresses it; taxonomizes satellite/UAV/HAPS/SAGIN work; lists open challenges including energy-aware semantic scheduling.
→ **Supports Sec. II (paper positioning):** cites as a recent survey that corroborates the "each NTN constraint maps to a SemCom fix" framing of the manuscript.

### 5. H. Peng, Z. Zhang, Y. Liu, Z. Su, T. H. Luan, and N. Cheng, "Semantic Communication in Non-Terrestrial Networks: A Future-Ready Paradigm," *IEEE Network*, vol. 38, no. 4, pp. 119–127, Jul. 2024. DOI: 10.1109/mnet.2024.3380817. https://www.comsoc.org/publications/best-readings/semantic-communications

Proposes an SC-based NTN architecture combining AI-driven semantic extraction with physical-layer security and semantic-aware resource management; the authors report experiments showing improved coverage efficiency and robustness in satellite–UAV–ground scenarios versus conventional communication.
→ **Supports Sec. II / extends [10][11]:** a peer-reviewed (ComSoc best-readings-listed) statement that semantic NTN is moving from vision to tested architecture — strengthens the paper's NTN relevance claim without re-citing Minani et al.

### 6. G. Zheng, Q. Ni, K. Navaie, and H. Pervaiz, "Semantic Communication in Satellite-Borne Edge Cloud Network for Computation Offloading," *IEEE J. Sel. Areas Commun.*, vol. 42, no. 5, pp. 1145–1158, May 2024. DOI: 10.1109/jsac.2024.3365879. https://doi.org/10.1109/jsac.2024.3365879

Studies semantic communication combined with edge-cloud computation offloading aboard satellites; jointly optimizes semantic extraction vs. offload decisions.
→ **Extends Sec. IV-E / Sec. VI-F:** a peer-reviewed instance of the exact compute-vs-radio trade-off the paper analyzes, but implemented on the satellite (edge cloud) side — useful contrast to the paper's ground-device-side framing.

### 7. P. Jiang, C.-K. Wen, X. Li, S. Jin, and G. Y. Li, "Semantic Satellite Communications Based on Generative Foundation Model," *IEEE J. Sel. Areas Commun.*, vol. 43, no. 7, pp. 2431–2445, Jul. 2025. DOI: 10.1109/jsac.2025.3559113. https://doi.org/10.1109/jsac.2025.3559113

Builds a satellite semantic-communication system on a generative foundation model that can reconstruct semantically rich content from very few transmitted features.
→ **Supports the Sec. III discussion of "raw-data fallback vs. semantic reconstruction":** a 2025 peer-reviewed proof that generative reconstruction at the receiver can substitute for transmitting the raw payload — the paper's most aggressive bandwidth claim.

### 8. W. Chen, S. Li, C. Ju, D. Wang, J. Li, and D. Wang, "Semantic-Enhanced Downlink LEO Satellite Communication System With OTFS Modulation," *IEEE Commun. Lett.*, vol. 28, no. 6, pp. 1377–1381, Jun. 2024. DOI: 10.1109/lcomm.2024.3386748. https://doi.org/10.1109/lcomm.2024.3386748

Adds semantic enhancement to a downlink LEO system using OTFS modulation (suited to high-Doppler LEO channels), showing semantic gains can coexist with delay-Doppler-domain waveforms.
→ **Supports Sec. IV-B (physical-layer assumptions):** relevant waveform-level evidence that semantic coding is compatible with LEO-friendly modulation — the paper's LEO link model should cite this rather than assuming away the waveform question.

---

## C. Lightweight semantic coding and the compute-vs-radio energy trade-off

### 9. Liu, An, Huang, and Yuen, "Over-the-Air ODE-Inspired Neural Network for Dual Task-Oriented Semantic Communications," *IEEE Trans. Cogn. Commun. Netw.*, early access, 2025. DOI: 10.1109/TCCN.2025.3569604. https://ieeexplore.ieee.org/document/11003068

Implements an ODE-inspired neural structure via over-the-air computation across distributed reconfigurable intelligent surfaces embedded inside a DeepSC-style pipeline, handling dual tasks (image reconstruction + semantic tagging) in one model; reports ~2× performance gain over an analog network without the Air-ODE structure.
→ **Supports Sec. III (semantic extractor design) with a caution:** an example of shrinking the semantic encoder via computation-in-the-channel; the paper should cite it as evidence that lightweight encoders are an active design target, but note the result is simulation-only and RIS-based (not NTN-applicable).

### 10. T. Wu, Z. Chen, M. Tao, Y. Sun, X. Xu, W. Zhang, and P. Zhang, "MambaJSCC: Adaptive Deep Joint Source-Channel Coding with Generalized State Space Model," arXiv:2409.16592, Sep. 2024. **[arXiv-only]** https://arxiv.org/abs/2409.16592 (code: https://github.com/wireless3c-sjtu/mambajscc)

Replaces transformer-based JSCC blocks with vision state-space (Mamba) blocks plus a CSI-adaptive module; the authors report it outperforms SwinJSCC with roughly 53% fewer MACs/parameters and ~45% lower inference delay, with reported experiments on a Jetson AGX Orin edge device.
→ **Supports Sec. III–IV:** the closest thing to hardware-grounded evidence for a lightweight semantic codec — but flag honestly that a Jetson AGX Orin is a 15–60 W edge computer, *not* an MCU-class NTN sensor, so the inference-energy numbers are not directly portable to the paper's Sec. IV-E model.

### 11. X. Chen, C. Huang, G. Chen, D. Feng, and P. Xiao, "The Communication and Computation Trade-Off in Wireless Semantic Communications," *IEEE Wireless Commun. Lett.*, vol. 14, no. 7, pp. 2259–2263, Jul. 2025. DOI: 10.1109/lwc.2025.3569205. https://doi.org/10.1109/lwc.2025.3569205

Analyzes where the compute-vs-transmit optimum lies for wireless semantic communications — i.e., when local semantic inference earns back more radio energy than it costs.
→ **Directly supports Sec. IV-E and Sec. VI-F:** a peer-reviewed statement of the paper's own break-even argument; cite it as independent corroboration of the claim that semantic coding only wins when inference energy < avoided radio energy.

### 12. Górecki, Hausman, and Korbel, "Cross-Layer Energy Management in Embedded AIoT Sensor Networks: A Structured Review, Full-Cycle Energy Model, and Break-Even Analysis," *Electronics*, vol. 15, no. 17, art. 4000, 2026. DOI: 10.3390/electronics15174000. https://www.mdpi.com/2079-9292/15/17/4000

Structured review (548 records screened, 56 sources) plus a full-cycle energy model and break-even analysis for on-device AI in sensor networks; an LTE-M experiment (40 transactions) shows payload length alone is insufficient to characterize communication energy — fixed overhead dominates for short packets (state-aware model R² = 0.980).
→ **Supports Sec. IV-E and the fixed-overhead H argument in Sec. VI-B/C:** peer-reviewed empirical backing that per-packet overhead dominates short-packet energy — exactly the regime where the paper's semantic-compression argument is strongest.

### 13. I. Lamaakal, C. Yahyati, Y. Maleh, K. El Makkaoui, and I. Ouahbi, "TinyHAR-UQ: Battery-aware, uncertainty-controlled tinyML for wearable activity recognition on IoT edge devices," *Internet of Things*, vol. 36, art. 101889, Mar. 2026. DOI: 10.1016/j.iot.2026.101889. https://doi.org/10.1016/j.iot.2026.101889

Deploys an int8 backbone with early exits and uncertainty-controlled inference on an nRF52840 (Cortex-M4F) and an ESP32-S3: 92.4–93.2% accuracy, 3–6 ms median (8–12 ms 95th percentile) latency, 0.54–0.92 mJ per inference window, 48–54 KB RAM, 210–215 KB flash.
→ **Supports Sec. IV-E with concrete numbers:** sub-1 mJ per MCU-class inference is peer-reviewed and measured — the paper can cite this as the realistic per-inference cost anchor for its break-even calculation (note: this is an activity-recognition task, so the numbers bound rather than equal a semantic encoder's cost).

---

## D. Application evidence — irrigation decisions and flood warnings

### 14. K. Taueatsoala, C. Daniels, A. J. Ramsunar, P. Bronkhorst, and A. E. Ezugwu, "TinyML-Enabled IoT for Sustainable Precision Irrigation," arXiv:2601.13054 [cs.LG], Jan. 2026. **[arXiv-only]** https://arxiv.org/abs/2601.13054

Edge-first irrigation framework: ESP32 microcontroller as the TinyML inference node plus a Raspberry Pi as local edge server, using soil moisture, temperature, humidity, pH, and ambient-light sensors; gradient boosting achieved R² = 0.9973 / MAPE 0.99%, the converted on-device ESP32 model predicts irrigation needs with MAPE < 1%, communication is MQTT over a LAN, and controlled-environment validation cut water use versus traditional methods. Fully offline-capable — no cloud dependency.
→ **Supports Sec. V-D (irrigation decision use case):** a 2026, India-relevant (resource-constrained smallholder) demonstration that the *decision* (irrigate / don't irrigate) can be made on-device with ~1% error — i.e., the exact "transmit the decision, not the data" traffic pattern the paper's semantic scheme assumes. Flag that validation is controlled-environment, not field-scale.

### 15. E. Artetxe, O. Barambones, I. Martín Toral, J. Uralde, I. Calvo, and A. del Rio, "Smart IoT Irrigation System Based on Fuzzy Logic, LoRa, and Cloud Integration," *Electronics*, vol. 13, no. 10, art. 1949, May 2024. DOI: 10.3390/electronics13101949. https://doi.org/10.3390/electronics13101949

LoRa-linked irrigation system driven by fuzzy logic with weather-forecast input, validated hardware-in-the-loop (dSPACE DS1104): 23.1% water-loss reduction versus on/off control over four days, plus 4.07% with forecast integration.
→ **Supports Sec. V-D:** a peer-reviewed, LoRa-based, hardware-in-the-loop quantification of what decision-driven irrigation saves (23.1% water loss) — gives the paper an independent, non-semantic baseline to beat in simulation.

### 16. V. Wiangnak, M. Wiboonrat, and S. Duangsuwan, "Development of an AIoT-Based Early Flash-Flood Warning System for Smart Rural Disaster Resilience," *Sensors*, vol. 26, no. 11, art. 3512, Jun. 2026. DOI: 10.3390/s26113512. https://doi.org/10.3390/s26113512

Deploys YOLOv10 visual water-level detection (precision/recall/mAP > 0.99) plus an LSTM water-level forecaster (R² 0.987/0.781) in a 60-day field deployment at two rural Thailand sites: detection probability > 0.92, critical success index > 0.82, 4–5 s end-to-end warning latency, >97% uptime.
→ **Supports Sec. V-E (flood-warning use case):** a 2026 field-deployed proof that edge AI + sensors delivers sub-5-second rural flood warnings with >0.92 detection — but note the limitation: it uses 5G/CCTV, not LPWAN/NTN, so the paper should present it as the *warning-latency/accuracy bar* its NTN semantic scheme must approach under far harsher link budgets.

---

## E. Surveys and prototypes

### 17. L. X. Nguyen, A. D. Raha, P. S. Aung, D. Niyato, Z. Han, and C. S. Hong, "A Contemporary Survey on Semantic Communications: Theory of Mind, Generative AI, and Deep Joint Source-Channel Coding," *IEEE Commun. Surveys & Tutorials*, vol. 28, 2026. DOI: 10.1109/comst.2025.3616973. https://doi.org/10.1109/comst.2025.3616973

2026 survey covering Theory-of-Mind semantic communication, generative-AI-based SemCom, and deep JSCC — the three strands the paper's Sec. II must distinguish itself from.
→ **Supports Sec. II:** cite as the up-to-date survey anchor so the paper only needs to position itself once, against a 2026 baseline rather than 2021–2023 surveys.

### 18. G. Fernandes, H. Fontes, and R. Campos, "Semantic Communications: the New Paradigm Behind Beyond 5G Technologies," arXiv:2406.00754, Jun. 2024. **[arXiv-only]** https://arxiv.org/abs/2406.00754

Survey that includes a prototypes/demonstrations section — SDR-based DeepJSCC testbeds and a facial-video semantic prototype among them.
→ **Supports the "experimental evidence" thread of the revision:** one of the few surveys cataloguing actual semantic-communication prototypes rather than pure theory; useful when the reviewers ask what has been built, not just simulated.

---

## Citation gaps the revision should address

1. **Goal-oriented random access with realistic MAC, beyond [9].** [9] (Delfani & Pappas 2025) is now complemented by DELTA (Chiariotti et al., INFOCOM 2025) and goal-oriented IRSA (Talli et al., arXiv 2026) — both ≥30% improvements in simulation over classical access, with DELTA using distributed belief/AoII and IRSA a VoI threshold broadcast. Neither is NTN-evaluated; the revision can cite them as the realistic MAC models the simulation should approximate, and note the NTN gap.
2. **Fixed-overhead dominance for short packets.** Górecki et al. (Electronics 2026) empirically show that for short IoT transactions, fixed communication overhead — not payload length — dominates energy. This is the peer-reviewed foundation for the paper's Sec. VI-B/C claim that semantic compression wins hardest on small packets; currently unsupported by measurement in the manuscript.
3. **Inference-energy vs. radio-savings break-even.** The paper's Sec. IV-E/VI-F argument is independently made by X. Chen et al. (IEEE Wireless Commun. Lett. 2025) and is anchored to measured MCU numbers by TinyHAR-UQ (0.54–0.92 mJ/inference on Cortex-M4F, Internet of Things 2026) and MambaJSCC (edge-device JSCC, ~53% fewer MACs). Cite all three; be explicit that no published measurement exists for a *semantic encoder* on an *MCU-class device over an NTN link* — the trace-driven simulation is the paper's contribution to filling that gap.
4. **Semantic NTN beyond Minani et al.** Peng et al. (IEEE Network 2024), G. Zheng et al. (JSAC 2024), and P. Jiang et al. (JSAC 2025) are all peer-reviewed 2024–2025 works that move semantic NTN from vision toward architecture and generative reconstruction. The revision should cite at least Peng and Jiang to show Sec. II is current to 2025, not stuck at [10][11].
5. **Irrigation decision reporting.** Taueatsoala et al. (arXiv 2026) and Artetxe et al. (Electronics 2024) give the paper what it lacks today: published, measured evidence that *on-device irrigation decisions* (MAPE < 1%; 23.1% water-loss reduction) are feasible — justifying the "transmit the decision" traffic model for Sec. V-D and the India lens.
6. **Flood-warning edge AI.** Wiangnak et al. (Sensors 2026) is a 60-day field deployment with 4–5 s warnings and >0.92 detection probability — a peer-reviewed performance bar for Sec. V-E. Its limitation (5G/CCTV, not LPWAN/NTN) must be stated; the paper's contribution is approaching that bar under NTN link budgets, not matching the setup.
7. **Remaining open gap (honest statement for the paper).** Across all four tracks, no 2024–2026 publication was found that measures a semantic/task-oriented encoder running on MCU-class hardware *over a real NTN or LPWAN link*. The closest evidence is either simulation (DELTA, GO-IRSA, Air-ODE, Agheli), edge-class hardware (MambaJSCC on Jetson), MCU-class inference on a non-semantic task (TinyHAR-UQ), or field AIoT on non-NTN links (flood warning). The revision's trace-driven simulation should be framed explicitly as narrowing this gap, with bounded claims.
