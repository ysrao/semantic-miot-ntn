# Track 4 — Critiques, limitations, and overclaiming risks in semantic communication

Supporting research for the revision of *"Application-Specific Semantic and Task-Oriented Communication for Massive IoT over NTN"* (working draft `/tmp/ntn_paper.txt`, read 2026-10-01).

Method note: this file is a literature-research digest, not a rewrite of the paper. Labels **[PR]** = peer-reviewed venue, **[PP]** = preprint/arxiv (not peer-reviewed at time of writing), **[OP]** = opinion/commentary (none used here). No quotes are invented; all summaries are paraphrases of the cited sources. Each entry ends with an **"Exact cautionary point for the target paper"** stating what the revision should do or avoid.

---

## Section 1 — Annotated critique bibliography (10 entries)

### 1. Misattribution: "semantic" gains are usually task-aware rate–distortion gains

**[PR]** D. Gündüz, Z. Qin, I. E. Aguerri, H. S. Dhillon, Z. Yang, A. Yener, K.-K. Wong, and C.-B. Chae, "Beyond Transmitting Bits: Context, Semantics, and Task-Oriented Communications," *IEEE J. Sel. Areas Commun.*, vol. 41, no. 1, pp. 5–41, Jan. 2023. doi: [10.1109/JSAC.2022.3223408](https://doi.org/10.1109/JSAC.2022.3223408); full text at https://discovery.ucl.ac.uk/id/eprint/10162483/1/Semantic_JSAC_SI_submitted.pdf

Summary: The most influential framework paper for task-oriented communication. It treats semantics operationally as a *generic (non-additive, non-single-letter) distortion measure* — i.e., semantic communication is a generalized rate–distortion problem, not a new physical-layer regime. The authors flag that the quantitative rate/resource relationship is "heavily tied with the downstream task," that precise theoretical guarantees for optimal rate and resource allocation "remain unsolved or even completely open," and that an optimized allocation strategy for one scenario generalizes poorly to others, so "a tradeoff between optimization and generalization needs to be explored."

**Exact cautionary point for the target paper:** Keep the II.B/VII framing that a gain is a *resource/task-outcome gain under a named task constraint*, never a Shannon-capacity increase. Cite this paper when stating that task-tied gains do not generalize across applications — it is the field's own flagship paper saying so, which defuses reviewer objections that the bounded framing is "too conservative."

### 2. "Breaking Shannon's limit" is a change of success criterion, not a capacity increase

**[PR]** G. Xin, P. Fan, and K. B. Letaief, "Semantic Communication: A Survey of Its Theoretical Development," *Entropy*, vol. 26, no. 2, Art. 102, 2024. doi: [10.3390/e26020102](https://doi.org/10.3390/e26020102); full text at https://mdpi-res.com/d_attachment/entropy/entropy-26-00102/article_deploy/entropy-26-00102.pdf?version=1706091364

Summary: A theory survey concluding that a complete theoretical framework for semantic communication "has yet to be established" and that finding its fundamental limits remains "very important yet still unresolved." Two findings matter here: (a) semantic channel capacity can be *higher or lower* than physical channel capacity depending on semantic ambiguity and KB quality — there is no theorem that it is always better; (b) the oft-repeated claim that semantic rate can exceed Shannon capacity holds only when a nonzero bit-error rate is tolerated while semantic error stays zero — i.e., the limit is "broken" by *changing the success criterion*, not by increasing physical capacity.

**Exact cautionary point for the target paper:** The draft's II.B/VI.G/IX language ("not an increase in physical-layer spectral efficiency or Shannon capacity") is exactly the correction this survey demands. Never let the words "semantic capacity" or "capacity gain" appear anywhere in the revision — reviewers will pounce on them. Any "supported devices per beam" result (IV.D) must remain labeled "effective task capacity," as it already is.

### 3. Reported gains come from shared knowledge/reasoning, not from the link

**[PP]** L. A. Lastras, B. M. Trager, J. Lenchner, W. Szpankowski, C. W. Wu, M. S. Squillante, and A. Gray, "Breaking through the classical Shannon entropy limit: A new frontier through logical semantics," arXiv:2501.00612, Dec. 2024. doi: [10.48550/arXiv.2501.00612](https://doi.org/10.48550/arXiv.2501.00612)

Summary: A Shannon-style analysis (IBM Research/Purdue) showing that communication efficiency gains from "semantics" arise when the receiver has *deductive reasoning capability* — the transmitted bits are magnified in value by shared logic and prior knowledge. The gain is thus attributable to the *knowledge base shared by both ends*, not to the channel; the same paper notes prior works treat semantics as a fidelity/distortion criterion inside rate–distortion theory rather than as something outside it.

**Exact cautionary point for the target paper:** Attribute the VI.B decomposition explicitly: the 1/q (suppression) gain is event/admission logic and the (H+Lraw)/(H+Lsem) gain is a shared-model compression gain. Add one sentence in II.B or VI.G stating that both mechanisms depend on a shared KB/model, so the "gain" is relative to the shared model — it evaporates under KB mismatch (ties directly to III.B/C and entry 5).

### 4. No universal metric: percentages across studies are incomparable

**[PP]** N. Tavakolian, H. Purmehdi, and J. Baek, "Rethinking Communication Metrics: How Should We Measure Meaning?" arXiv:2608.21626, Aug. 2026. https://arxiv.org/abs/2608.21626

Summary: An evaluation-centered survey (not architecture-centered) concluding that evaluation of semantic communication is fragmented across telecom, NLP, CV, and ML, and "no single metric can characterize semantic quality across modalities, tasks, and channel conditions." Specific warnings: semantic KPIs lack standardized measurement procedures, can give *conflicting* assessments of the same output, and can shift when their underlying embedding models are updated; *semantic drift* occurs when sender/receiver KBs or models evolve independently or the environment changes (e.g., an encoder trained on one domain deployed in another); application-specific success criteria must be agreed in advance; open problems include no universal success criteria, no standardized ground truth, and weak integration of ML metrics with communication constraints.

**Exact cautionary point for the target paper:** This is the strongest published backing for three things the draft already does: (a) the II.A disclaimer that the cited 50%/73%/87.5%/4x percentages "are not reproduced or combined here" — keep it and add one clause citing metric-incomparability; (b) V.A's fixed-operating-point comparison design — label it as the recommended response to the metric problem; (c) V.D/V.E's warning that a model trained for one district/season must not be assumed valid elsewhere — that is literally the paper's "semantic drift" case.

### 5. KB mismatch creates a new, silent error class

**[PR]** (conference) paper on language mismatch for multiuser semantic communication, presented at IEEE ISWCS 2024; full text https://export.arxiv.org/pdf/2405.20085. The result is worth citing for the mechanism: when the language generator (transmitter) and interpreter (receiver) are *not trained jointly*, a semantic mismatch arises *even if training uses the same architectures, data, and objectives*, because the latent-space partitions misalign; the authors compensate with semantic channel equalization over a codebook of linear transformations.

Summary: Knowledge-base divergence between transmitter and receiver is not a corner case — it is the default whenever models are trained, versioned, or updated independently. Mismatch produces *confident misinterpretation*: bits arrive correctly but meaning does not. The compensation requires extra signaling/model alignment, i.e., KB management has a communication cost that must appear in the energy/traffic budget.

**Exact cautionary point for the target paper:** III.B/C's model-identifier/fallback design is well motivated; strengthen it by (a) citing this mismatch mechanism, (b) evaluating *undetected* drift in VII.C's holdout experiments (the draft already proposes "fallback policy evaluated under detected and undetected drift" — keep that sentence; it is exactly right), and (c) accounting model-update/distribution traffic in the energy model (eq. 5 mentions model updates; VIII.C lists "model-training and update energy" as separate evidence — fine, keep the boundary explicit).

### 6. On-device inference energy can erase radio savings — break-even analysis required

**[PR]** S. Górecki, S. Hausman, and P. Korbel, "Cross-Layer Energy Management in Embedded AIoT Sensor Networks: A Structured Review, Full-Cycle Energy Model, and Break-Even Analysis," *Electronics*, vol. 15, no. 17, Art. 4000, 2026. doi: [10.3390/electronics15174000](https://doi.org/10.3390/electronics15174000); https://www.mdpi.com/2079-9292/15/17/4000

Summary: A structured review (548 screened records, 56 coded sources) that coins "semantic compression" for replacing raw measurements with inferred descriptors and states explicitly that *its energy benefit is not automatic*: acquisition, preprocessing, model execution, radio wake-up, signaling, and retransmission energy must jointly stay below the avoided communication energy. The break-even analysis shows the admissible local-processing budget is *bounded by the fixed (per-message) communication overhead* — when H dominates, per-byte savings buy little energy. An LTE-M experiment (40 full transactions) found payload length alone *insufficient* to characterize communication energy; a state-aware model with signaling duration reached R² = 0.980.

**Exact cautionary point for the target paper:** This is the published warrant for eq. (5), the VI.F break-even discussion, and VII.D's rule that modeled energy is reported as *sensitivity ranges, not hardware claims*. Add a citation here; and note the LTE-M finding as justification for V.B's required sensitivity sweep over fixed overhead H — because when H is large, even large q and L gains produce small energy savings, which is the honest story the reviewers will test.

### 7. Security/privacy: semantic content leaks even when bits are protected

**[PP]** R. Meng et al., "A Survey of Secure Semantic Communications," arXiv:2501.00842, Jan. 2025. http://arXiv.org/abs/2501.00842

Summary: Surveys security/privacy across the full SemCom lifecycle (training, model transfer, transmission). Threats include model inversion, adversarial and backdoor attacks, and privacy inference on transmitted semantic features; a transmitted semantic label/decision (e.g., fault state, location, irrigation decision) can itself be the sensitive asset, so link-layer confidentiality does not imply semantic privacy.

**Exact cautionary point for the target paper:** VIII.B already states "Confidentiality of raw data does not guarantee semantic privacy" — keep that sentence and cite this survey. Extend the evaluation requirements (VII) with one line: report the effect of spoofed/forged urgency or confidence metadata on beam resources (the draft already raises this in VIII.B) and of model-poisoning on task loss, since VIII.A's utility-based scheduler is only as trustworthy as its inputs.

### 8. Semantic eavesdropping defeats conventional physical-layer security assumptions

**[PP]** "When Eavesdroppers Reason: Agentic Eavesdropping Attacks on Semantic Communication," arXiv:2605.02204 (2025/2026). https://arxiv.org/pdf/2605.02204v1

Summary: Shows eavesdroppers can recover recognizable source information from intercepted semantic transmissions *even at low SNR (~0 dB)*, via simple decoders or model-inversion attacks enhanced with generative priors (privacy inference success reported at 80–100% in the surveyed work); conventional physical-layer security, which relies on a channel advantage over the eavesdropper, is insufficient because semantic decoders extract meaning from heavily degraded signals.

**Exact cautionary point for the paper:** For NTN downlinks — inherently broadcast — this strengthens the VIII.B security paragraph: semantic NTN needs semantic-level confidentiality/integrity, not just link encryption. Do not claim semantic reporting is "more private" than raw reporting; argue the opposite as a limitation to be engineered around (aligns with the paper's honest tone and III.B's auditable-fallback requirement).

### 9. "Semantic" report suppression is largely event-triggered sampling — a decades-old mechanism

**[PR]** Classic networked-control literature, e.g., K. J. Åström and B. Bernhardsson (2002) on event-based sampling (Lebesgue sampling) showing smaller state variance than periodic sampling at the same average rate; M. Rabi, K. H. Johansson et al. (2008) on event-triggered sensing/actuation for networked control; and the survey line in networked-control reviews distinguishing time-triggered (Riemann) from event-triggered (Lebesgue) sampling, the latter "significantly reduc[ing] the network traffic volumes." Representative accessible references: the IFAC/UST review at http://eeqiu.people.ust.hk/wp-content/uploads/2021/04/Time-and-Event-Based-Sensor-Scheduling-for-Networks-with-Limited-Communication-Resources.pdf and the Sensors 2018 review https://www.mdpi.com/1424-8220/18/8/2547.

Summary: Transmitting only when a significant change or event occurs — the mechanism behind the draft's 1/q report-suppression factor — has been studied in control and sensor networks since the early 2000s (and in industrial deadband reporting practice far longer). It is a real, measured gain, but it is *not* a gain attributable to "semantics" or to AI.

**Exact cautionary point for the target paper:** II.B's rule — "The comparison must also separate semantic gain from ordinary compression and event triggering" — is the single most reviewer-proof sentence in the draft; elevate it from related work into the evaluation requirements (it already appears in V.A and VII.C as reference mechanisms — keep both, and make the ablation in VII.C mandatory rather than conditional: change "may be included" to "shall be included"). Credit the mechanism honestly: report suppression = event-triggered admission; payload reduction = task-aware compression.

### 10. Overclaiming language exists in the literature — a concrete example of what to avoid

**[PP]** (unifying survey) "Semantic Edge Computing and Semantic Communications in 6G Networks: A Unifying Survey and Research Challenges," arXiv:2411.18199. https://arxiv.org/pdf/2411.18199v3

Summary: A useful survey of the three-level (technical/semantic/task) model, semantic noise, and KB-update requirements — but it also contains, verbatim, the sentence "Such systems can break the Shannon's limit by transmitting only the semantic meaning behind the message instead of raw bits." Per entries 1–2, that sentence is exactly the overclaim this revision must avoid: it conflates a changed success criterion with a capacity increase.

**Exact cautionary point for the target paper:** Use as the negative example in the related-work discussion: the draft's position (gain = resource-utilization/task-outcome gain, II.B) should be contrasted with this phrasing to show reviewers the authors know the difference. Never let "break/beyond Shannon" appear in the revision.

### Also consulted (background, not primary critique sources)

- **[PR]** T. M. Getu, G. Kaddoum, and M. Bennis, "Making sense of meaning: A survey on metrics for semantic and goal-oriented communication," *IEEE Access*, vol. 11, pp. 45456–45492, 2023. doi: [10.1109/ACCESS.2023.3269933](https://doi.org/10.1109/ACCESS.2023.3269933) — documents that the lack of unified/universal metrics "can stifle research progress." (Already cited as [5] in the draft.)
- **[PR]** W. Yang et al., "Semantic communications for future internet: Fundamentals, applications, and challenges," *IEEE Commun. Surveys Tuts.*, vol. 25, no. 1, pp. 213–250, 2023 — general challenges survey.
- **[PP]** S. Mukherjee, "Transformers for Green Semantic Communication: Less Energy, More Semantics," arXiv:2310.07592, Oct. 2023. https://doi.org/10.48550/arXiv.2310.07592 — proposes an "Energy-Optimized Semantic Loss" multi-objective loss jointly optimizing semantic loss and energy consumption, noting the absence of universal metrics for the joint effect. Useful methodological precedent for the checklist's joint energy+quality reporting.

---

## Section 2 — CLAIMS TO SOFTEN OR CUT

The draft is already unusually careful (II.B, VI, IX use explicit bounded language). The items below are residual vulnerabilities — mostly small rewordings, not cuts. Section references are to the draft.

1. **II, related-work percentages ("reduced the energy arrival rate required … by 50%", "73% reduction", "87.5% lower transmission delay", "four times as many users").** The draft already says these "are not reproduced or combined here" (II.A) — keep that, and add one clause citing entry 4: *"published percentages use mutually incomparable metrics and baselines, so they are cited as directional evidence only."* This preempts the reviewer who notes that [6]–[9] measure different things.

2. **VI.E, the 32.5× illustrative calculation.** Well bounded in the text ("illustrative offered-byte ratio, not a measured NTN capacity result"). Residual risk: a large ratio in the body *will* be quoted out of context as the paper's result. Recommended rewording of the VI.E closing: append *"This ratio is a teaching example, not a finding; the revision's measured results will be reported per Section VII with the attributions of Section II.B."* If a reviewer already flagged numbers, consider moving the worked example to an appendix — but do not delete it; the decomposition pedagogy (entry 3) is valuable.

3. **II.B / V.A / VII.C: "Conventional compression and deterministic event triggering are retained only as reference mechanisms *where relevant* / *may be included*."** "Where relevant/may" is the soft spot entry 9 attacks. Recommended rewording (VII.C): *"The ablation always includes deterministic event triggering and conventional compression baselines, so that any residual gain can be attributed to the semantic/task-oriented mechanism rather than to ordinary compression or report suppression."*

4. **V.C application hypotheses ("may obtain larger report suppression", "may provide larger payload reduction").** These are correctly phrased as hypotheses. Guard them by adding the entry-1/4 caveat once: *"These hypotheses are expected to be application-specific and non-transferable across the five classes."* Do not let any of them harden into a claimed result in the conclusion.

5. **III.A/III.D, "self-evolving" / "self-evolution" terminology.** The mechanism described is actually *guarded closed-loop adaptation with validated redeployment* — the draft says so, but the word "self-evolving" invites a reviewer to read "unconstrained online learning." Recommended: rename to "controlled adaptation (two time scales)" and keep the guardrail sentences verbatim. Nothing substantive changes; the hype-adjacent label goes.

6. **III.A, "assigns confidence and urgency."** Assumes calibrated confidence is available on-device. Entries 4–5 (metric instability, silent KB mismatch) make *uncalibrated confidence* a failure mode. Recommended addition (one sentence in III.B or VII.C): *"Confidence values must be calibration-validated on the deployment distribution; uncalibrated confidence is treated as a fault input, triggering conservative fallback."*

7. **V.I, population-scale arithmetic ("One million sensors reporting every 15 min generate 96 million reports/day…").** Already labeled "offered-traffic calculations, not claims of supported beam capacity." Keep the label; add "not a deployment claim" wording consistent with the "methodological stress range" phrasing already used for the 10³–10⁶ sweep.

8. **VIII.B, metadata security paragraph.** Currently says "may require integrity and replay defense" and notes semantic-privacy limits — good, but "may" undersells entries 7–8 for a broadcast NTN downlink. Recommended rewording: *"requires integrity and replay protection, because forged urgency/confidence can exhaust shared beam resources; evaluation includes spoofed-metadata and model-poisoning cases."* This turns a limitation paragraph into a reviewer-satisfying evaluation requirement.

9. **Cut candidate: any sentence implying semantic reporting is inherently more private or more secure than raw reporting.** The draft does not currently make this claim — verify it stays that way in the rewrite (entries 7–8 argue the opposite is often true).

10. **X, conclusion metric list (1)–(8).** Fine as a reporting checklist, but add the entry-4 consequence: metrics (4) "task-throughput efficiency" and (5) "supported devices per beam" must be reported *with the named application, dataset, task constraint, energy model, access configuration, and load range attached* (the IX bounded-language rule) — i.e., never as bare percentages.

## Section 3 — Honest evaluation checklist for the revision's simulation

Grounded in the sources above; each item cites its warrant.

1. **Fix the task operating point before measuring anything.** Select and freeze task-accuracy, missed-event probability, and deadline constraints first; measure payload, report rate, airtime, and energy *at that common point* for every scheme (draft V.A; warranted by entries 1, 4 — without this, "gain" is just discarding task-required information).
2. **Mandatory ablation separating the two gain mechanisms.** Always report (a) semantic payload coding, (b) report admission/suppression, (c) scheduling-metadata effects, and (d) retraining/model-distribution traffic separately; credit ordinary compression and deterministic event triggering where they explain the result (draft VII.C; warranted by entries 3, 9).
3. **Baselines must include the strong conventional alternatives, not strawmen.** Raw payload reporting, conventional compression, and deterministic event triggering at the *same* task-quality operating point, on the *same* sensor trace and channel realization (draft V.A, VII.A; warranted by entry 9).
4. **Uncertainty quantification with adequate event counts.** Report seeds, mean/median, and confidence intervals; for rare-event miss probabilities, require enough events to support the stated precision — otherwise report a bound or refrain (draft VII.D; entry 4's reproducibility concern).
5. **Full-cycle energy accounting as sensitivity ranges, not hardware claims.** Include sensing, inference, memory, access, transmission, retransmission, idle, *and* model-update distribution energy; state whether values are measured, trace-derived, or modeled; present modeled values as sweeps (especially over fixed overhead H and inference energy), because break-even is bounded by per-message overhead (draft IV.E, VII.D; warranted by entry 6).
6. **Evaluate under KB mismatch and undetected drift.** Include temporal/geographic holdout and silent-degradation runs; require the fallback policy to be exercised under *undetected* drift, and report the resulting task loss, not just the detected case (draft III.B/C, VII.C; warranted by entry 5).
7. **Adversarial and privacy evaluation of the semantic layer.** Test forged urgency/confidence metadata (beam-exhaustion), model-poisoning effects on task loss, and privacy leakage of semantic labels/decisions even under link encryption (draft VIII.B; warranted by entries 7, 8).
8. **No universal percentages; stratify every claim.** Report gains per application, dataset, task constraint, energy model, access configuration, and offered-load regime (including correlated-burst and near-saturation regimes with widened confidence intervals); never use "capacity gain" or "beyond Shannon" language — the permitted term is *resource-utilization/task-outcome gain* (draft IX; warranted by entries 1, 2, 4, 10).
