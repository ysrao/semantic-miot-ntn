# Track 1 — Real NTN IoT Deployments & Measurements (2022–2026)

Literature research for the revision of *"Application-Specific Semantic and Task-Oriented Communication for Massive IoT over NTN."*
Compiled 2026-10-01. Prioritizes peer-reviewed and standards sources; vendor claims are labeled as such.
All URLs verified against the search result they were copied from.

---

## Section 1 — 3GPP NTN-IoT timeline

| Release | Frozen | NTN-IoT content | Status |
|---|---|---|---|
| **17** | Stage-3 protocol freeze Mar 2022 (TSG#95); ASN.1 coding freeze Jun 2022 (TSG#96) | TR 36.763 study (2021) → normative NB-IoT/eMTC over satellite: L/S-band (bands n255/n256), transparent (bent-pipe) payload as the Rel-17 focus, Earth-fixed beams prioritized, UE GNSS-based timing/frequency pre-compensation, HARQ feedback may be disabled (reliability via RLC AM + blind repetitions), extended timers. | **Specified & frozen.** Commercial chipsets/modules shipping (e.g., Nordic nRF9151, Sony/Murata/Skylo-certified modules). |
| **18** | Functional freeze Dec 2023; RAN ASN.1 freeze Jun 2024 | NTN Phase 2: IoT-NTN optimizations — NTN coverage enhancements, TN↔NTN mobility procedures, GNSS power optimization, new scenarios/bands; plus NR-NTN throughput/performance work and Ka-band direction. | **Specified & frozen.** IoT-NTN Phase 2 folded into the 3GPP NTN program page. |
| **19** | Scheduled functional completion Q4 2025 | IoT_NTN_Ph3 (RP-234077): **Store & Forward (S&F) operation based on regenerative payload** including feeder-link switchover; **uplink capacity enhancements**. NR_NTN_Ph3 (RP-234078) runs in parallel (regenerative payload, ISL via Xn). Iridium's NB-IoT extensions accepted as an official Rel-19 work item (Sep 2024). | **Standardization complete/near-complete; not yet commercial.** Implementations, chipset support, and deployments of S&F/regenerative IoT-NTN are pre-commercial as of Oct 2026. |

**Key verdict:** NB-IoT NTN is commercially *specified* (Rel-17/18) and commercially *deployed* — 3GPP's own NTN page states: "With IoT-NTN specified in 3GPP RAN Rel-17, with optimizations following in Rel-18, commercial deployments are now ongoing." Regenerative-payload and store-and-forward operation (the architecture most relevant to sparse LEO IoT constellations) was only *specified* in Rel-19, not deployed.

**Sources**
- 3GPP, "5G Non-Terrestrial Networks" (official technologies page; cites IoT_NTN_Ph3 RP-234077 and NR_NTN_Ph3 RP-234078): https://www.3gpp.org/technologies/5g-ntn
- 3GPP TR 36.763, "Study on NB-IoT/eMTC support for NTN," Rel-17, 2021 (cited in paper as [1]).
- Release 17 freeze dates (Stage 3 Mar 2022; ASN.1 Jun 2022): https://www.rcrwireless.com/20220325/5g/what-the-timeline-3gpp-release-17 ; https://blog.3g4g.co.uk/2022/04/3gpp-release-17-5g-nr-reaches-completion.html
- Rel-18 freeze (Dec 2023 functional; ASN.1 Jun 2024): http://standards-tracker.5g-ppp.eu/online-tool-standards-tracker/summary-report-3gpp-plenaries-mainly-ran-98e-electronic-meeting-12-16
- Rel-19 Q4 2025 schedule + Iridium work item: https://iotbusinessnews.com/2024/09/25/05605-iridium-accelerates-direct-to-device-service-with-acceptance-into-3gpp-standards-announces-iridium-ntn-direct/
- Rel-19 S&F and uplink-capacity scope: https://www.3gpp.org/technologies/5g-ntn (IoT_NTN_Ph3 description)

---

## Section 2 — Operator-by-operator status

Legend: ✅ operating (paying customers / live traffic) · 🧪 trial/lab · 📣 announced/pre-commercial · ❌ retired

### ✅/🧪 Skylo Technologies — operating (GEO, 3GPP NB-NTN)
- **Model:** No satellites of its own; virtual NTN operator leasing capacity on existing GEO satellites (Inmarsat/Viasat-class MSS spectrum).
- **Protocol:** Standards-based 3GPP NB-IoT NTN (NB-NTN) over GEO; works with Rel-17-level commercial NB-IoT chipsets, no special antenna/modem.
- **Scale:** Claims >8M activated devices on its NTN; regulatory approvals in 36 countries using MSS spectrum. Demonstrated first commercial voice calls over NB-NTN (Skylo Voice Gateway, AI codec; >10× data reduction claimed — vendor claim); NB-NTN voice submitted as a 3GPP Rel-20 work item (approved Jun 2025).
- **Commercial proof:** Soracom (KDDI) partnership — limited preview 2024 → **General Availability Oct 3, 2025** in North America, Europe, Latin America, Oceania; hybrid terrestrial+satellite NB-IoT under one SIM/CMP.
- **Caveat for modeling:** GEO link — RTT ~540 ms, very low data rates (see §3: 80 b/s single-carrier at 23 dBm in link-budget studies; measured 200 B message latency 13–35 s).
- Sources: https://www.thefastmode.com/technology-solutions/44265-skylo-enables-first-commercial-voice-calls-over-nb-ntn-satellite-network ; https://www.rcrwireless.com/20240717/internet-of-things/soracom-offers-satellite-nb-iot-from-skylo-in-phased-commercial-launch ; https://www.thefreelibrary.com/Soracom+Launches+Integrated+Satellite+IoT+Connectivity+Solution+with...-a0858227125

### 🧪/✅ Sateliot (Spain) — early commercial, discontinuous LEO
- **Constellation:** 6 satellites launched of 68 planned (250 ultimate), "GroundBreaker" phase; launches ongoing (newspace.im census, Jul 2026). Altitude class ~500–600 km LEO.
- **Protocol:** 3GPP Rel-17 NTN NB-IoT; standard commercial NB-IoT devices connect "without any modification." Uses partner MNO terrestrial spectrum via roaming.
- **Architecture:** Explicitly **discontinuous coverage + store-and-forward** — the first LEO constellation operating 3GPP Rel-17 NTN this way.
- **Status:** Commercial service launched on sparse constellation; €30M EIB loan; Series C raising €100M (2026); ESA-selected for sovereign connectivity (RESCUE-NET under IRIS²); next-gen Tritó satellites planned 2027 with 5G NR D2D.
- **Modeling relevance:** This is the closest real-world instance of the paper's scenario — NB-IoT over sparse LEO with store-and-forward and hours-scale contact gaps.
- Sources: https://telecomdrive.com/sateliot-selected-by-esa-for-sovereign-connectivity-programme/ ; https://www.bnamericas.com/en/news/sateliot-and-grupo-constanta-join-forces-to-connect-the-groups-infrastructure-in-brazil ; https://www.newspace.im/assets/fig/Newspace_constellations_direct-to-cell_2026-07-31.pdf

### 🧪/✅ OQ Technology (Luxembourg) — operating, 3GPP LEO
- **Constellation:** 10 LEO satellites in orbit; plan for 72.
- **Spectrum/protocol:** 60 MHz of priority MSS S-band globally; **3GPP-based 5G NB-IoT NTN**. Dec 2025: demonstrated end-to-end 5G NB-IoT link with a standard Nordic Semiconductor nRF9151 terrestrial chipset, no hardware modification.
- **Commercial:** Services live in Saudi Arabia (Aramco), Rwanda, Nigeria, Australia (S-band license secured Sep 2025); roaming agreements with 20+ telcos (KPN, Deutsche Telekom, Telefónica, EMnify). D2D text messaging targeted end of 2026 (announced; pre-commercial).
- Sources: https://spacenews.com/oq-technology-expands-satellite-iot-services-to-australia/ ; https://www.lightreading.com/satellite/oq-technology-raises-25m-to-launch-more-5g-d2d-satellites ; https://satnews.com/2025/12/19/oq-technology-integrates-terrestrial-chipsets-for-mass-market-ntn-iot/

### ✅ Iridium — operating (proprietary); standards-based NTN in development
- **Constellation:** 66 operational L-band LEO satellites (~780 km) + spares; truly global, real-time (cross-linked).
- **Current IoT:** Proprietary services operating for decades — SBD short-burst data, Iridium Edge modules. ~1,300 SOS/emergency incidents per year handled.
- **NTN Direct (Project Stardust):** Standards-based 5G NB-IoT NTN D2D on the existing constellation. 3GPP accepted Iridium's NB-IoT extension as a Rel-19 work item (Sep 2024). Lab demo done 2024; **testing in 2025, commercial rollout targeted 2026** — still in technical development as of latest announcements. Mavenir converged packet core selected (Feb 2025) to enable 3GPP D2D.
- **Corporate:** Rocket Lab agreed to acquire Iridium (~$8B, announced Jun 2026 — reported; verify before citing as fact).
- Sources: https://www.satellitetoday.com/connectivity/2024/09/25/iridium-plans-standards-based-service-ntn-direct/ ; https://www.sdxcentral.com/news/iridium-plans-new-direct-to-device-nb-iot-satellite-service/ ; https://www.verdict.co.uk/iridium-project-stardust-service/

### ✅ Globalstar — operating (proprietary)
- **Constellation:** 2nd-generation LEO (~1,414 km); 25 satellites launched of 42 (53 incl. spares) per newspace.im.
- **IoT:** Proprietary one-way (Simplex) + two-way (Duplex) LEO IoT, long-established in asset tracking. **RM200M two-way satellite IoT module commercially launched Oct 21, 2025** (globally certified; GNSS + BLE + app processor on-module). Powers iPhone satellite messaging.
- **Corporate:** Amazon agreed to acquire Globalstar (~$11.6B, announced Apr 2026 — reported, pending; verify before citing).
- Sources: https://markets.financialcontent.com/custercountychief/article/marketminute-2025-10-21-globalstar-soars-on-commercial-launch-of-global-satellite-iot-module ; https://www.newspace.im/assets/fig/Newspace_constellations_direct-to-cell_2026-07-31.pdf

### ❌ Swarm (SpaceX) — retired
- 189 VHF nanosatellites; proprietary IoT modems. **Dedicated-modem IoT service shut down in 2025**, folded into Starlink Direct-to-Cell. (Source: https://en.wowtale.net/2026/09/26/235230/ ; newspace.im lists "Retired, Acquired".)

### 🧪 Astrocast (Switzerland) — operating but fragile
- ~20 nanosatellites in orbit (500–600 km LEO) of an 80-satellite target; **proprietary L-band protocol** (Astronode S), bidirectional.
- Counterpoint Research (Sep 2026) still rates Astrocast an active "challenger" in satellite IoT. newspace.im (Jul 2026) census: 20/80, "Launches ongoing, **Unknown**" — financing/launch cadence uncertain; treat forward-looking claims cautiously.
- Sources: https://spacenews.com/astrocast-raises-9-2-million-grows-target-iot-constellation-size-to-80-satellites/?via=indexdotco ; https://www.mobileworldlive.com/industry/iridium-skylo-top-satellite-iot-tables/ ; https://www.newspace.im/assets/fig/Newspace_constellations_iotm2m_2026-07-31.pdf

### 🧪 Lacuna Space (UK) — operating, LoRa-based (not 3GPP)
- 12 satellites of 240 planned; **LoRa/LoRaWAN via satellite** — proprietary LPWAN adaptation, not 3GPP NB-IoT.
- Source: https://www.newspace.im/assets/fig/Newspace_constellations_iotm2m_2026-07-31.pdf

### 📣 EchoStar / Hughes / EchoStar Mobile — waiting, not deployed
- EchoStar holds global S-band rights for D2D/IoT but has deployed nothing; CEO (May 2026): "If I had a satellite today, I would not launch it today" — waiting for the NTN-compatible device installed base; insists on 3GPP-standard handsets.
- EchoStar Mobile pursuing pan-European **LoRa NTN** (per ABI Research, May 2025) — non-3GPP path.
- Mavenir + Terrestar conducted first NB-IoT live data sessions via the **Echostar T1 GEO** satellite (Feb 2025) — lab/trial, not commercial.
- SpaceX agreed to acquire ~$20B of EchoStar spectrum (2025).
- Sources: https://www.kratosspace.com/constellations/articles/echostar-on-its-direct-to-device-plans-were-not-standing-still-were-lying-in-wait ; https://www.globenewswire.com/search/tag/satellitecommunication ; https://iotbusinessnews.com/2025/05/15/15159-hot-tech-innovators-abi-research-names-globalstar-iridium-and-echostar-mobile-among-8-top-satellite-operators-innovating-in-the-iot-market/

### 📣 Ligado — niche/stalled
- GEO (ex-SkyTerra) L-band North America. ~2019 partnership (Ericsson + Sequans) for NB-IoT over satellite never reached commercial service. Counterpoint (Sep 2026) rates Ligado a **niche** player. No operating NB-IoT NTN service as of 2026.

### Market-level snapshot (Sep 2026)
Counterpoint Research: **Iridium and Skylo are the "pacesetters"** in satellite IoT; Viasat, Globalstar, Orbcomm, Myriota "leaders"; **Sateliot, OQ Technology, Astrocast "challengers"**; Terrestar, Ligado among seven "niche" players. Research director: the satellite IoT sector "is still at a nascent stage." (Source: https://www.mobileworldlive.com/industry/iridium-skylo-top-satellite-iot-tables/)

---

## Section 3 — Parameter table

Values a trace-driven NTN-IoT simulation can defend. "Confidence" is *measured* (field/hardware), *specified* (3GPP), *simulated* (peer-reviewed system/link simulation), or *estimated* (computed from geometry — method shown).

| # | Parameter | Defensible value / range | Exact source (where the number appears) | Confidence |
|---|---|---|---|---|
| 1 | NB-IoT NTN uplink rate, LEO, 23 dBm | **1.28 kb/s** single-carrier (3.75 kHz); **8.2 kb/s** with 3 subcarriers | Mannoni et al., "System Level Evaluation for NB-IoT Satellite Communications," IEEE VTC2022-Spring, Table III (PHY configurations derived from the authors' PIMRC 2021 link-budget/PER analysis) | Simulated (link-budget-driven) |
| 2 | NB-IoT NTN uplink rate, GEO, 23 dBm | **80 b/s** single-carrier | Same, Table III | Simulated |
| 3 | NPRACH repetitions | 1 (LEO config) / 8 (GEO 23 dBm config); standard allows **up to 128** per attempt | Same, Table III; Cluzel et al. HAL paper notes up to 16-repetition reference waveforms | Simulated / specified |
| 4 | NPUSCH/NPDCCH repetitions | NPDCCH 4 (LEO) / 64 (GEO 23 dBm); NPUSCH format-1 up to 128 max (DCI Format N0) | Mannoni et al., Table III and §II-B ("Each TB … is repeated (DCI Format N0, 128 max.)") | Simulated / specified |
| 5 | NPRACH periodicity / NPDCCH period | NPRACH period **1280 ms**; NPDCCH period 32 ms (LEO) / 128 ms (GEO) | Mannoni et al., §III-B | Simulated (configuration choice) |
| 6 | Random-access + setup time **T_RA**, LEO (low load) | Sync 2560 ms + RA procedure ~400 ms + security/attach/auth + data ~2025 ms → **~5 s end-to-end** for a 300 B message (23 dBm); rises to ~25 s at 600+ users/spot | Mannoni et al., §III-C, Fig. 6 ("The average time to connect and to transmit the data is between around 5 s when low numbers of users are considered") | Simulated |
| 7 | End-to-end latency, GEO (low load) | **66 s** at 23 dBm; 24 s (27 dBm); 19 s (30 dBm) — low users; network sync + RA alone 8.9 s (23 dBm) | Mannoni et al., §III-C, Fig. 7 | Simulated |
| 8 | **Measured** GEO NB-NTN attach | Mean **93.3 s**, 6,656 mAs (max 11,290 mAs), RSRP −120…−126 dBm | Richter, "Practical Performance Analysis of NB-IoT across Terrestrial and Non-Terrestrial Networks," bachelor thesis 2026, §4.3.1 Table 5 (COTS NB-IoT modem, field measurements, Leipzig; GEO NB-NTN PLMN 90198) | **Measured** (field) |
| 9 | **Measured** GEO NB-NTN payload latency | 200 B: median **34.9 s** (linear antenna; upper quartile 46.2 s, max 70.5 s) → **13.4 s** with directive circular-polarized antenna (max 18.7 s). 500 B: 47.6 s → 20.6 s. | Same thesis, §4.4, Figs. 20–21 | **Measured** (field) |
| 10 | **Measured** message drop rate, GEO | 9.0% (13/144) linear antenna → ~1.1% (2/174, 2/198) circular antenna | Same thesis, §4.4 | **Measured** (field) |
| 11 | Protocol overhead per message | TCP over GEO NTN: **147% overhead**, frequent timeouts; CoAP/UDP: reliable, no loss observed. Attach/auth message sizes: Msg3 88 bits, Auth Req 336 bits, Attach Accept 800 bits, BSR 32 bits; a 300 B UE message sent as **8 NPUSCH packets of 328 bits**. | Thesis §4.2.1 (TCP/CoAP); Mannoni et al., Table II | Measured / simulated |
| 12 | TX power | **23 dBm (200 mW)** power class 3 (highest standard NB-IoT class; Sørensen et al. note it explicitly). Mannoni et al. also evaluate proposed 27/30 dBm classes (not standard). | Sørensen et al., "NB-IoT for NTN LEO" (Small Satellite Conf. 2021, arXiv:2108.06172): "The highest power class in NB-IoT is power class 3 (PC3) — 23 dBm, 200 mW" | Specified |
| 13 | **Measured** NTN energy per attach | **6,656 mAs mean** (~1.85 mAh) | Richter thesis, §4.3.1 | **Measured** (field) |
| 14 | **Measured** NTN energy per payload | 150 B: 4,843 mAs (33.8 s active); 250 B: 9,083 mAs (59.9 s); 750 B: 15,872 mAs (105.5 s); mean draw **155–168 mA** (max TX power) | Same thesis, §4.3.2, Table 6 | **Measured** (field) |
| 15 | NTN energy multipliers vs terrestrial | Attach: **~110×** optimal-TN attach (≈0.68× worst-case edge-of-cell TN attach). Payload TX: **150× (150 B) to 400–420× (250–750 B)** vs optimal TN; **13× to 30–38×** vs edge-of-cell TN. | Same thesis, §4.3.4 | **Measured** (field) |
| 16 | LEO RTT, ~600 km | **4.0 ms** (zenith) to **12.9 ms** (10° elevation, 1,932 km slant) | Computed from circular-orbit geometry (R=6,371 km, c); consistent with Mannoni et al. Table I distances for 770 km LEO (780–2,617 km → 5.2–17.4 ms RTT) | Estimated (geometry) |
| 17 | GEO RTT | **≥500 ms** (250 ms one-way transparent case cited; ~540 ms typical bent-pipe round trip) | Richter thesis §2.1.1; Barbau et al., "NB-IoT over GEO Satellite" (HAL hal-03080712): "minimum 125 ms (GEO regenerative) or 250 ms (GEO transparent) one-way" | Specified / measured-context |
| 18 | LEO pass duration, 600 km, fixed ground point | **12.8 min** max (horizon-to-horizon); **~8.5 min** above 10° elevation | Computed (see §4 note); consistent with Cakaj, "Practical horizon plane and communication duration for LEO satellite ground stations" (contact 5–15 min), and Mannoni et al. (≤12 min per passage at 770 km) | Estimated + literature |
| 19 | Passes/day, single satellite over fixed point | **~4–8** usable passes per day (polar LEO, ground station) | Cakaj 2009 (WSEAS Trans. Commun.): "contact communication time … (5–15) minutes … 6–8 times during the day" | Literature (measured/analytical) |
| 20 | Per-spot (beam) visibility, LEO | **45 s (central spot) to 3.5 min (peripheral)**; average **<1 min for 50%** of cases — i.e., a device may *not* finish a full attach+data transaction within one spot pass (NB-IoT has no handover) | Mannoni et al., §II-A, Fig. 2 | Simulated (Kepler/orbital mechanics) |
| 21 | Orbital period, 600 km | **96.5 min** (~14.9 orbits/day) | Computed; cf. Britannica LEO fact sheet (LEO periods 90 min–2 h) | Estimated + literature |
| 22 | Supported devices per spot (300 B, 30 msg/day) | LEO: **660 users/spot** (23 dBm) → 890 (27/30 dBm). GEO: **115** (23 dBm) → 3,000 (27/30 dBm). Global: 31M (LEO, 23 dBm) / 66M (27 dBm) with 66 sats; GEO 0.23M–4.85M with 3 sats | Mannoni et al., §III-C, Fig. 8 | Simulated |
| 23 | NB-IoT air interface basics | 180 kHz carrier; UL single-tone 3.75 kHz; 3 coverage-enhancement classes; max coupling loss ~164 dB (Rel-13 design target) | Cluzel et al., "3GPP NB-IoT coverage extension using LEO satellites" (HAL hal-02059933), Table II; 3GPP Rel-13 design targets | Specified |
| 24 | Device duty-cycle reality check | LoRa-via-Iridium study: 2,400 mAh battery ≈ **1 year** at one transmission per 100 min (satellite LoRaWAN) | Cited in "Pervasive LPWAN connectivity through LEO Satellites" (HAL hal-03844534), §2 | Literature (measured) |

**Numbers I could not source — stated explicitly as unavailable:**
- Per-message *protocol overhead in bytes* for a 3GPP Rel-17 NTN attach on a live commercial network (the thesis measured total energy/time, not byte-level signaling breakdown; Mannoni Table II gives simulated message sizes).
- Commercially observed NPRACH collision rates or RA success probability on Skylo/Sateliot/OQ live networks (no public data).
- Live-network repetition factors actually configured by Skylo/Sateliot (not disclosed).
- Device-side inference energy for semantic models on NTN chipsets (no published measurements found; must be modeled as a sensitivity range per the paper's own §VII-D rule).

---

## Section 4 — Honest assessment: real vs aspirational

**What is real today.** 3GPP Rel-17/18 NB-IoT NTN is a finished, specified standard with shipping chipsets, and commercial service genuinely exists: Skylo's GEO NB-NTN (live, multi-region, GA via Soracom Oct 2025), Sateliot's and OQ Technology's sparse LEO constellations running 3GPP NB-IoT with real customers, and decades-old proprietary LEO IoT (Iridium, Globalstar). Counterpoint (Sep 2026) still calls the whole sector "nascent," which is fair — constellations number in the single digits to tens of satellites, not thousands.

**What is aspirational.** Continuous, real-time LEO NTN-IoT coverage; regenerative payloads and Rel-19 store-and-forward operation (specified, not deployed); Iridium NTN Direct (testing 2025, commercial target 2026); NB-NTN voice (demonstrated, Rel-20 work item); EchoStar's entire D2D plan (explicitly on hold). Vendor capacity claims (e.g., "tens of millions of calls per month per region") are marketing, not measurements.

**Assumptions in the paper that need softening for the revision:**
1. **Contact windows are discontinuous and sparse.** For Sateliot-class constellations (6 sats), a device sees a handful of short passes per day with hours-scale gaps — model store-and-forward with per-pass completion probability, not a continuously available beam. Mannoni et al. show a device may not even finish one attach+data transaction inside a single spot pass (45 s–3.5 min per spot; no NB-IoT handover).
2. **T_RA and H dominate tiny payloads — which actually strengthens the paper's core argument.** Measured/simulated setup is seconds (LEO ~5 s) to ~1.5 min (GEO attach), versus sub-second-to-seconds of payload airtime; measured GEO payload energy is 10–40× edge-of-cell terrestrial. The gain mechanism is therefore overwhelmingly *report suppression* (N_x), not payload shrinking (L_x) — the simulation should say so explicitly and credit suppression first.
3. **The energy model must include attach/access energy as a first-class term.** Measured NTN attach costs ~6,656 mAs (~1.85 mAh) — comparable to transmitting hundreds of bytes. For LEO with moving beams, attach/auth transactions recur per new satellite/spot. E_access must be parameterized from these measurements, not just E_tx.
4. **Reliability comes from blind repetitions, not HARQ.** Rel-17 NTN disables HARQ feedback; reliability is via RLC AM + preconfigured repetitions (up to 128). The retransmission term E_retx in Eq. (5) should be reframed as repetition overhead K plus RLC-ARQ residual.
5. **Present all modeled numbers as ranges with the measured anchors.** The strongest defensible anchors are: 23 dBm TX, 1.28 kb/s LEO / 80 b/s GEO single-carrier rates, ~5 s LEO / ~13–66 s GEO message latency, ~155–168 mA active draw, and the 10–40× energy multipliers — each traceable to the table above.
