#!/usr/bin/env python3
"""Build the SPACOMM 2027 (IARIA) submission Word document.

IARIA format: US Letter, two columns, 10pt Times New Roman, single-spaced,
justified, first-line indent, no page numbers, max 6 pages (+4 extra at fee).
Abstract style: "Abstract - ..."; Keywords: "Keywords-a; b; c."
"""
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
import re, os

FIGDIR = "/home/hatch/workspace/ntn-eval/figures"
OUTDIR = "/home/hatch/workspace/ntn-eval/paper"
os.makedirs(OUTDIR, exist_ok=True)

doc = Document()

# ---------------------------------------------------------------- base style
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(10)
st.paragraph_format.space_after = Pt(0)
st.paragraph_format.space_before = Pt(0)
st.paragraph_format.line_spacing = 1.0
st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
st.paragraph_format.first_line_indent = Pt(10)
st.paragraph_format.widow_control = True
# ensure East Asia / complex script fonts too
rpr = st.element.get_or_add_rPr()
for tag in ("w:rFonts",):
    el = rpr.find(qn(tag))
    if el is None:
        el = rpr.makeelement(qn(tag), {})
        rpr.append(el)
    el.set(qn("w:ascii"), "Times New Roman")
    el.set(qn("w:hAnsi"), "Times New Roman")
    el.set(qn("w:cs"), "Times New Roman")

for i in range(1, 4):
    hs = doc.styles[f"Heading {i}"]
    hs.font.name = "Times New Roman"
    hs.font.bold = True
    hs.font.size = Pt(11 if i == 1 else 10)
    hs.paragraph_format.space_before = Pt(0)
    hs.paragraph_format.space_after = Pt(6)
    hs.paragraph_format.first_line_indent = Pt(0)
    hs.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hs.paragraph_format.keep_with_next = True

# ---------------------------------------------------------------- page setup
sec0 = doc.sections[0]
sec0.page_width = Mm(215.9)
sec0.page_height = Mm(279.4)
for s in (sec0,):
    s.top_margin = Mm(25)
    s.bottom_margin = Mm(25)
    s.left_margin = Mm(20)
    s.right_margin = Mm(20)
    s.header_distance = Mm(12)
    s.footer_distance = Mm(12)

def no_indent(p):
    p.paragraph_format.first_line_indent = Pt(0)
    return p

def para(text, bold_prefix=None, size=10, italic=False, align=None, before=0, after=0):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Pt(10)
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    if align is not None:
        p.paragraph_format.alignment = align
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
        r.font.size = Pt(size)
        r.font.name = "Times New Roman"
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.name = "Times New Roman"
    r.italic = italic
    return p

def h1(t):
    return doc.add_heading(t, level=1)

def h2(t):
    return doc.add_heading(t, level=2)

def eq(t):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(t)
    r.font.size = Pt(10)
    r.font.name = "Times New Roman"
    return p

def fig(path, caption, width_in=3.34):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_picture(path, width=Mm(width_in * 25.4))
    c = doc.add_paragraph()
    c.paragraph_format.first_line_indent = Pt(0)
    c.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_before = Pt(6)
    c.paragraph_format.space_after = Pt(6)
    r = c.add_run(caption)
    r.font.size = Pt(8)
    r.font.name = "Times New Roman"
    return p

def set_columns(section, n):
    cols = section._sectPr.xpath("./w:cols")[0]
    cols.set(qn("w:num"), str(n))
    if n == 2:
        cols.set(qn("w:space"), "340")  # 6 mm in twentieths of a point

def table(caption, headers, rows, fontsize=8):
    s1 = doc.add_section(WD_SECTION.CONTINUOUS)  # full-width table
    set_columns(s1, 1)
    c = doc.add_paragraph()
    c.paragraph_format.first_line_indent = Pt(0)
    c.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_before = Pt(6)
    c.paragraph_format.space_after = Pt(4)
    r = c.add_run(caption)
    r.font.size = Pt(8)
    r.font.name = "Times New Roman"
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    t.autofit = True
    for j, htxt in enumerate(headers):
        cell = t.rows[0].cells[j]
        cell.text = ""
        pr = cell.paragraphs[0]
        pr.paragraph_format.first_line_indent = Pt(0)
        pr.paragraph_format.space_after = Pt(1)
        pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = pr.add_run(htxt)
        run.bold = True
        run.font.size = Pt(fontsize)
        run.font.name = "Times New Roman"
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            cell = t.rows[i].cells[j]
            cell.text = ""
            pr = cell.paragraphs[0]
            pr.paragraph_format.first_line_indent = Pt(0)
            pr.paragraph_format.space_after = Pt(1)
            pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = pr.add_run(val)
            run.font.size = Pt(fontsize)
            run.font.name = "Times New Roman"
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    s2 = doc.add_section(WD_SECTION.CONTINUOUS)  # back to two columns
    set_columns(s2, 2)
    return t

# ================================================================ TITLE BLOCK
t = doc.add_paragraph()
t.paragraph_format.first_line_indent = Pt(0)
t.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
t.paragraph_format.space_after = Pt(10)
r = t.add_run("From Illustrative to Measured: Task-Oriented Semantic mIoT over NTN for Remote Agriculture and Environmental Sensing")
r.bold = True
r.font.size = Pt(16)
r.font.name = "Times New Roman"

a = doc.add_paragraph()
a.paragraph_format.first_line_indent = Pt(0)
a.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
a.paragraph_format.space_after = Pt(2)
r = a.add_run("Rao Yenamandra, Mubanga Nsofu, Ram Asokan")
r.font.size = Pt(11)
r.font.name = "Times New Roman"

a2 = doc.add_paragraph()
a2.paragraph_format.first_line_indent = Pt(0)
a2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
a2.paragraph_format.space_after = Pt(2)
r = a2.add_run("DigitalTwinSim \u2014 San Diego, CA, USA; Vodacom \u2014 Johannesburg, South Africa; "
              "Wireless Research Center of North Carolina \u2014 USA")
r.font.size = Pt(10)
r.font.name = "Times New Roman"

a3 = doc.add_paragraph()
a3.paragraph_format.first_line_indent = Pt(0)
a3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
a3.paragraph_format.space_after = Pt(8)
r = a3.add_run("raosy@digitaltwinsim.com; mubanga.nsofu@vodacom.co.za; asokan.ram@wrc-nc.org")
r.font.size = Pt(10)
r.font.name = "Times New Roman"

para("Non-terrestrial networks extend sixth-generation connectivity to massive Internet of Things "
     "deployments beyond economical terrestrial coverage, but periodic short reports incur "
     "disproportionate access, protocol, repetition, and retransmission overhead. This paper presents "
     "a measured evaluation of application-specific semantic and task-oriented reporting for massive "
     "Internet of Things over non-terrestrial networks, narrowed to two India-oriented applications: "
     "irrigation decisions for smart agriculture and flood warnings for environmental monitoring. "
     "Device or gateway intelligence extracts task-relevant features, estimates observation value and "
     "urgency, and admits only reports whose expected value justifies their access and airtime cost. "
     "A three-stage trace-driven simulation compares semantic reporting against raw periodic, "
     "compressed periodic, and event-triggered baselines under common task-quality, reliability, and "
     "deadline constraints. The measured offered-byte gain of 42.6\u00d7 is dominated by report "
     "suppression (18.9\u00d7) rather than payload shrinkage (2.25\u00d7). Supported devices per beam "
     "increase from 50 to 1,600 for irrigation, while conventional periodic reporting cannot meet the "
     "flood-warning deadline at any modeled population. Semantic operation improves correct, timely "
     "task outcomes per unit of radio resource when the task tolerates sparse reporting; raw-data "
     "fallback remains required for audit, drift, and billing.",
     bold_prefix="Abstract - ")

para("massive Internet of Things; non-terrestrial networks; semantic communication; "
     "task-oriented communication; satellite Internet of Things.",
     bold_prefix="Keywords-")

# ------------------------------------------------- switch to two columns
sec1 = doc.add_section(WD_SECTION.CONTINUOUS)
sec1.top_margin = Mm(25); sec1.bottom_margin = Mm(25)
sec1.left_margin = Mm(20); sec1.right_margin = Mm(20)
sec1.header_distance = Mm(12); sec1.footer_distance = Mm(12)
cols = sec1._sectPr.xpath("./w:cols")[0]
cols.set(qn("w:num"), "2")
cols.set(qn("w:space"), "340")  # 6 mm in twentieths of a point

# ================================================================ I
h1("I. INTRODUCTION")
para("Non-terrestrial networks (NTNs) extend massive Internet of Things (mIoT) connectivity to "
     "agriculture, environmental monitoring, logistics, maritime operations, and utilities that cannot "
     "be served economically by dense terrestrial deployments. Third Generation Partnership Project "
     "(3GPP) Release 17 work on Narrowband Internet of Things (NB-IoT) and enhanced Machine Type "
     "Communication (eMTC) established a standards foundation for Internet of Things over satellite "
     "access [1], and the International Telecommunication Union vision for IMT-2030 identifies massive "
     "communication, ubiquitous connectivity, sustainability, and artificial intelligence as central "
     "sixth-generation (6G) directions [2], [3].")
para("Coverage alone does not solve the scaling problem. A satellite beam aggregates very large "
     "populations of low-duty-cycle devices, each generating short messages that incur random-access, "
     "protocol, repetition, and retransmission overhead. Periodically conveying every sensed value "
     "treats the NTN as a content-unaware bit pipe even when the application needs only a decision: "
     "whether irrigation is required, or whether a flood threshold was exceeded. The cost is "
     "unnecessary terminal energy, satellite airtime, contention, queueing, storage, and processing.")
para("Semantic communication seeks to convey meaning rather than reproduce every source bit, whereas "
     "task-oriented (goal-oriented) communication optimizes the receiver's ability to complete an "
     "application objective [4], [5]. For mIoT the distinction is operationally useful: semantics "
     "determine what information is relevant, and task orientation determines whether that information "
     "deserves immediate NTN resources. This paper develops an application-specific framework "
     "connecting these ideas to measurable radio-access quantities: task throughput, supported devices "
     "per beam, and total device energy.")
para("Recent studies report large improvements: a semantics-aware low-Earth-orbit update policy halved "
     "the required energy arrival rate for a target information age [6]; a query-aware "
     "terrestrial/non-terrestrial formulation cut the charging rate by 73% [7]; an Open RAN-enabled "
     "semantic NTN study reported up to 87.5% lower delay [8]. These figures are cited as directional "
     "evidence only. This paper instead starts from two observable changes\u2014bytes per admitted "
     "report and reports admitted per unit time\u2014and converts them into measured task outcomes per "
     "unit of radio resource under fixed task-quality, reliability, and deadline constraints, with "
     "conventional compression and deterministic event triggering retained as mandatory baselines.")
para("The contributions are: (i) a narrowed, India-oriented evaluation on two applications\u2014"
     "irrigation decisions and flood warnings\u2014replacing an earlier illustrative treatment; "
     "(ii) a three-stage trace-driven simulation reporting means and standard deviations over five "
     "held-out seeds, including negative and break-even findings; (iii) an explicit attribution showing "
     "that the measured gain comes overwhelmingly from report suppression rather than payload "
     "shrinkage; and (iv) a complete reproducibility package. The work addresses the SPACOMM 2027 "
     "track on global coverage via 6G/7G through integration of 5G and Internet of Things with "
     "satellite networks. The paper claims no increase in physical-layer spectral efficiency: the "
     "reported gains are resource-utilization and task-outcome gains, as formalized in Section II.")

# ================================================================ II
h1("II. RELATED WORK AND RESEARCH GAP")
h2("A. Semantic, Goal-Oriented, and Task-Oriented Communication")
para("The shift beyond bit-level fidelity has been motivated as a possible 6G transition beyond the "
     "separation of source meaning from channel delivery [4]. Metrics span semantic similarity, "
     "information freshness, value, task accuracy, and goal effectiveness [5], consolidated in a recent "
     "survey [9].")
para("Task-tied gains generalize poorly across scenarios: the field's flagship treatment presents "
     "semantic communication as generalized rate-distortion and warns of a tradeoff between "
     "optimization and generalization [10]. Semantic channel capacity can be higher or lower than "
     "physical capacity depending on semantic ambiguity and knowledge-base quality; claims of "
     "exceeding the Shannon limit hold only when the success criterion itself is changed [11]. "
     "Published percentage improvements use mutually incomparable metrics and baselines [12]. This "
     "paper therefore treats its bounded framing\u2014gains reported per application, dataset, task "
     "constraint, energy model, access configuration, and load range\u2014as consensus rather than "
     "timidity.")
h2("B. Semantic Communication over NTN")
para("Goal-oriented medium access has been demonstrated with anomaly-triggered reporting driven by "
     "distributed belief about information correctness, improving on classical random access in large "
     "networks [13]. Semantic quality-aware resource allocation for NTN downlinks has been studied "
     "[14], [15], and a semantic communication architecture for non-terrestrial networks with "
     "AI-driven extraction and semantic-aware resource management has been evaluated experimentally "
     "in satellite\u2013UAV\u2013ground scenarios [16]. Source-side packet admission and drop rules "
     "that maximize a semantic-utility objective formalize which packets deserve airtime [17].")
h2("C. NTN IoT Link and Energy Reality")
para("System-level simulation of NB-IoT over low-Earth orbit reports a 1.28 kb/s single-carrier "
     "uplink at 23 dBm, about 5 s end-to-end for a 300-byte message at low load, 660\u2013890 supported "
     "users per spot, and per-spot visibility of only 45 s to 3.5 min [18]. Field measurements over a "
     "commercial geostationary NB-IoT link report a mean attach time of 93.3 s costing about 1.85 mAh, "
     "and payload transmission energy 150\u2013420 times that of an optimal terrestrial link [19] "
     "(bachelor-thesis field measurements, cited as measured rather than peer-reviewed evidence). The "
     "implication, verified against both sources, is that access and setup dominate tiny payloads: the "
     "gain mechanism available to semantic reporting is overwhelmingly report suppression, not payload "
     "shrinkage. 3GPP Release 17 specifies bent-pipe NB-IoT NTN operation with disabled hybrid "
     "repeat-request and blind repetitions, while Release 19 store-and-forward operation is specified "
     "but not yet deployed [1]; the sparse low-Earth-orbit scenario in this paper is therefore "
     "standards-track rather than commercial reality.")
para("On the energy side, per-packet fixed overhead dominates short-packet communication energy, as "
     "shown empirically for LTE-M [20]; the communication-versus-computation tradeoff has been "
     "analyzed to locate where local semantic inference earns back more radio energy than it costs "
     "[21]; and int8 tiny machine-learning inference on Cortex-M4F hardware costs 0.54\u20130.92 mJ "
     "per inference [22]\u2014an anchor that bounds, rather than equals, a semantic encoder's cost, "
     "since no published measurement of a semantic encoder on microcontroller-class hardware over a "
     "non-terrestrial link was found. Information freshness metrics and their variants [23] are used "
     "only where appropriate to the application; for alarms, detection delay and missed-alarm "
     "probability are more meaningful.")
h2("D. Application Evidence")
para("For irrigation, edge-first tiny machine-learning nodes have demonstrated on-device "
     "irrigation-need prediction with mean absolute percentage error below 1% in controlled "
     "environments [24]\u2014exactly the \u2018transmit the decision, not the data\u2019 traffic pattern "
     "assumed here. For flood warning, a 60-day field deployment of an AI-of-Things flash-flood system "
     "achieved detection probability above 0.92 [25]; that system used fifth-generation and camera "
     "links, so this paper's contribution is to approach comparable task performance under NTN link "
     "budgets, not to match the setup.")
h2("E. Research Gap")
para("Event-triggered (Lebesgue) sampling\u2014transmitting only on significant change\u2014predates "
     "semantic communication by decades and is a measured, real gain not attributable to semantics or "
     "artificial intelligence [26]. Any semantic claim must therefore survive comparison against "
     "deterministic event triggering and conventional compression; this paper makes those ablations "
     "mandatory. Across the surveyed literature, no 2024\u20132026 publication was found that measures "
     "a semantic or task-oriented encoder running on microcontroller-class hardware over a real "
     "non-terrestrial or low-power wide-area link. The present work narrows that gap with a "
     "trace-driven simulation whose link and energy models are anchored in the measurements above, "
     "reporting honest negatives alongside gains.")

# ================================================================ III
h1("III. FRAMEWORK AND MODELS")
h2("A. Functional Architecture")
para("Figure 1 shows the architecture. A semantic agent at the device or village gateway observes the "
     "application state, extracts a compact representation, assigns calibrated confidence and urgency, "
     "and decides what task-relevant information, if any, should cross the constrained NTN hop: a "
     "compact feature, an event or state summary, or a final task decision. An access controller "
     "admits a message only when its expected value at delivery justifies the access, airtime, "
     "energy, and collision cost. The receiving edge application decodes the semantic content, "
     "performs task inference, and returns task-accuracy feedback through a guarded learning loop; "
     "verified model updates travel outside the urgent short-packet path. Raw or losslessly "
     "compressed data remain available as fallback for audit, drift diagnosis, billing, and forensic "
     "analysis. Inference may reside at the sensor, gateway, satellite payload, or terrestrial edge, "
     "but only processing before the constrained hop can suppress traffic on that hop.")
fig(os.path.join(FIGDIR, "fig1_architecture_v2.png"),
    "Figure 1. Application-specific semantic / task-oriented mIoT over NTN: field sensing, "
    "on-device semantic agent, LEO uplink, edge task engine, and guarded learning loop.")
h2("B. Traffic, Airtime, Throughput, and Energy Models")
para("For reporting scheme x, let Nx be the number of reports in an observation interval, Lx the "
     "application payload bytes per report, and H the fixed protocol, access, and framing overhead "
     "per report. The offered information volume is")
eq("Bx = Nx(H + Lx).   (1)")
para("Let TRA be the random-access and setup time, Kx the repetition factor, and R the effective "
     "transmission rate. The airtime per admitted report is")
eq("Tmsg,x = TRA + Kx[8(H + Lx)/R].   (2)")
para("Semantic communication does not normally increase R; its resource gain comes from fewer "
     "reports and fewer bytes per admitted report. The task-oriented throughput efficiency is the "
     "number of correct, timely application outcomes per occupied radio resource,")
eq("\u03b7TO,x = Cx/[W \u03a3 Tmsg,x].   (3)")
para("where Cx counts only outcomes meeting the accuracy, missed-event, reliability, confidence, and "
     "deadline constraints, and W is the occupied bandwidth. The first-order supported device "
     "population per beam is")
eq("Mmax,x \u2264 \u03c1Tobs/(\u03bbxTmsg,x).   (4)")
para("with per-device report rate \u03bbx, usable beam-airtime fraction \u03c1, and observation interval "
     "Tobs. This is an effective task-capacity relation, not Shannon capacity. Total device energy "
     "over the interval is")
eq("Ex = Esense + EAI,x + Eaccess,x + Etx,x + Eretx,x + Eidle.   (5)")
para("Access energy Eaccess,x is a first-class term: measured non-terrestrial attach costs about "
     "1.85 mAh [19], comparable to the energy of hundreds of payload bytes. The net saving is "
     "SE = 1 \u2212 Esem/Eraw; device-side intelligence is beneficial only when avoided access, "
     "transmission, and retransmission energy exceeds added inference energy. A scheme is feasible "
     "only when")
eq("maximize \u03b7TO,x  s.t. E[lossx] \u2264 \u03b5, Pmiss,x \u2264 \u03b4miss, Pr(dx \u2264 D) \u2265 1 \u2212 \u03b4D.   (6)")
h2("C. Gain Decomposition")
para("The semantic report fraction q = Nsem/Nraw = \u03bbsem/\u03bbraw (7) is the fraction of "
     "conventional reports still crossing the NTN link. The offered-byte gain")
eq("GB = Braw/Bsem = (H + Lraw)/[q(H + Lsem)]   (8)")
para("decomposes as GB = (1/q) \u00d7 [(H + Lraw)/(H + Lsem)]: report-suppression gain times "
     "per-report payload gain. The airtime gain")
eq("Gair = Traw,total/Tsem,total = Tmsg,raw/[qTmsg,sem] \u2248 Msem/Mraw   (9)")
para("is smaller whenever fixed access time, repetitions, or collisions matter. The "
     "task-throughput-efficiency gain")
eq("GTO = \u03b7TO,sem/\u03b7TO,raw = (Csem/Craw)Gair   (10)")
para("is valid only when the semantic scheme preserves correct, timely outcomes. As a teaching "
     "example only, Lraw = 200 B, Lsem = 20 B, H = 60 B, q = 0.1 gives")
eq("GB,illustrative = 260/8 = 32.5.   (11)")
para("a 10\u00d7 suppression gain times a 3.25\u00d7 size gain. This ratio is a teaching example, not "
     "a finding; measured results are reported in Section V with the attributions of Section II.")
h2("D. Controlled Adaptation, Trust, and Interfaces")
para("Adaptation runs on two time scales under the name controlled adaptation. Fast operation "
     "executes the deployed, validated model and policies for inference, admission, and scheduling "
     "without modifying weights. Slow operation adapts thresholds and policies\u2014and, when evidence "
     "warrants, retrains models\u2014over hours to weeks; only validated updates return to the fast "
     "loop. Audit records retain source time, model version, threshold, confidence, selected mode, "
     "access attempts, and receiver outcome, supporting rollback.")
para("A semantic decision can be wrong even when its bits arrive correctly. Confidence values must "
     "therefore be calibration-validated on the deployment distribution; uncalibrated confidence is "
     "treated as a fault input that triggers conservative fallback. Model identifiers and validity "
     "intervals provide knowledge consistency and trigger raw or feature-level fallback on mismatch. "
     "Because forged urgency or confidence could exhaust shared beam resources, semantic metadata "
     "requires integrity and replay protection. Confidentiality of raw data does not guarantee "
     "semantic privacy: a transmitted irrigation decision or flood label can itself be the sensitive "
     "asset.")

# ================================================================ IV
h1("IV. EVALUATION DESIGN")
h2("A. Applications")
para("Two India-oriented applications are evaluated. (i) Smart agriculture: irrigation decisions from "
     "soil-moisture, rainfall, humidity, and temperature traces generated by a water-balance model "
     "with calibrated noise, stratified into dry, normal-rainfall, irrigation, heavy-rain, and monsoon "
     "regimes. The task rule\u2014a soil-moisture deficit threshold with two-sample persistence, "
     "hysteresis, and causal moving-average smoothing\u2014issues irrigate/defer decisions; quality is "
     "measured by recall, missed-stress events, false alarms per week, and detection delay. "
     "(ii) Environmental monitoring: flood warnings from rainfall-intensity and river-level traces "
     "generated by a leaky-integrator model with calibrated noise, including geographically correlated "
     "monsoon bursts; quality is measured by warning recall, missed-event probability, false alarms "
     "per week, and detection delay against a 45-minute deadline. Traces are synthetic; the India "
     "lens enters through regime stratification and application parameters, not through claimed sensor "
     "datasets.")
para("Device and receiver use the identical decision rule, so the measured semantic gain comes from "
     "where and when data are sent, not from a smarter receiver model. Thresholds are tuned on seeds "
     "101\u2013105 and evaluated on held-out seeds 201\u2013205.")
h2("B. Baselines")
para("Four modes share the same trace, channel realization, bandwidth, terminal power, access "
     "procedure, repetitions, visibility, and deadline: raw periodic (96 reports/day, 260 B), "
     "compressed periodic (2:1), deterministic event-triggered, and semantic/task-oriented (admitted "
     "reports of 80 B, six-hourly heartbeats, and one daily raw audit sample). Compression and "
     "event triggering are mandatory ablations: any residual gain is attributable to the "
     "semantic/task-oriented mechanism rather than to ordinary compression or report suppression "
     "[26].")
h2("C. NTN Scenario")
para("The configured sparse low-Earth-orbit scenario uses a 600 km orbit, 48 passes per day of 900 s "
     "(beam-airtime fraction \u03c1 = 0.5), 180 kHz carrier, 16 kbps, a 2 s random-access slot, at most "
     "3 attempts per pass with retries across passes, slotted-ALOHA access with geometric retries, "
     "blind repetitions (hybrid repeat-request disabled per [1]), and store-and-forward across "
     "discontinuous contact windows. This is a single plausible scenario, not a multi-constellation "
     "sweep.")
h2("D. Reproducibility")
para("The simulation is a deterministic Python package (run_all.py, about 2.5 min) with fixed seeds, "
     "YAML configurations, a requirements file, result CSVs, and figure scripts in ~/workspace/ntn-eval. "
     "Energy figures are modeled NB-IoT-class values (sensing 2 mJ, inference 0.1\u20131 mJ, access "
     "250 mJ/attempt, transmission 0.5 \u00b5J/bit, idle 15 \u00b5W)\u2014presented as sensitivity ranges, "
     "not hardware claims.")

# ================================================================ V
h1("V. MEASURED RESULTS")
para("All numbers below are measured from the simulation (mean \u00b1 standard deviation over the five "
     "held-out seeds 201\u2013205), not assumed.", after=4)
h2("A. Stage 1: Offered Load and Suppression")
para("Table I reports deterministic byte and report accounting. For irrigation, semantic reporting "
     "admits q = 0.053 of raw reports (5.1 versus 96.0 per day), giving GB = 42.6 \u00b1 0.1 and "
     "Gair = 19.6 \u00b1 0.1. The decomposition of (8) attributes 18.9\u00d7 to report suppression and "
     "only 2.25\u00d7 to payload shrinkage (260 B to 80 B): suppression dominates, as the "
     "measurement-anchored model predicts. The fixed 60 B header caps the airtime gain below the byte "
     "gain (19.6 < 42.6); sweeping H = 20/60/120 B moves GB through 55.2/42.6/34.5. Flood-warning "
     "results are nearly identical (GB = 42.3 \u00b1 0.2, Gair = 19.4 \u00b1 0.2). Event-triggered "
     "reporting already captures most of the admission gain for flood warnings (q = 0.047, "
     "GB = 22.1 \u00b1 5.2) but transmits full raw payloads on each trigger; for irrigation it fires "
     "far more often (q = 0.365) because the trigger rule lacks the semantic rule's smoothing and "
     "hysteresis. Figure 2 shows the decomposition.")
table("TABLE I. STAGE-1 OFFERED LOAD AND SUPPRESSION (MEAN \u00b1 SD OVER 5 SEEDS)",
      ["App", "Mode", "Rep./day", "kB/day", "q", "GB", "Gair"],
      [["Agri", "raw", "96.0", "24.96", "1.000", "1.0", "1.0"],
       ["Agri", "compr. 2:1", "96.0", "15.36", "1.000", "1.6", "1.0"],
       ["Agri", "event-trig.", "35.1", "9.12", "0.365", "2.7 \u00b1 0.1", "2.7 \u00b1 0.1"],
       ["Agri", "semantic", "5.1", "0.59", "0.053", "42.6 \u00b1 0.1", "19.6 \u00b1 0.1"],
       ["Env", "raw", "96.0", "24.96", "1.000", "1.0", "1.0"],
       ["Env", "compr. 2:1", "96.0", "15.36", "1.000", "1.6", "1.0"],
       ["Env", "event-trig.", "4.5", "1.18", "0.047", "22.1 \u00b1 5.2", "22.1 \u00b1 5.2"],
       ["Env", "semantic", "5.1", "0.59", "0.053", "42.3 \u00b1 0.2", "19.4 \u00b1 0.2"]])
fig(os.path.join(FIGDIR, "fig1_suppression_decomposition.png"),
    "Figure 2. Stage-1 gain decomposition (irrigation): 18.9\u00d7 report suppression \u00d7 2.25\u00d7 "
    "payload shrinkage = 42.6\u00d7 offered-byte gain; the fixed 60 B header caps the airtime gain at 19.6\u00d7.")
h2("B. Stage 2: NTN Access and Supported Population")
para("Sweeping device population until deadline success falls below 0.95 gives the supportable "
     "population M\u2217. For irrigation (6 h deadline), M\u2217 rises from 50 (raw periodic) to 200 "
     "(event-triggered) to 1,600 (semantic)\u2014an 8\u00d7 gain over the strongest baseline. For flood "
     "warnings (45 min deadline), raw and compressed periodic reporting collapse to M\u2217 = 0: at "
     "even 50 devices per beam, congested slotted-ALOHA access (about 0.9 Erlang offered load) cannot "
     "meet the deadline with 95% reliability. Semantic reporting supports 400 devices per beam where "
     "the conventional baseline supports none; event-triggered supports 800 (400 under burst). "
     "Figures 3\u20135.")
fig(os.path.join(FIGDIR, "fig2_airtime_vs_load.png"),
    "Figure 3. Airtime versus offered load: semantic reporting keeps per-device airtime low as "
    "population grows, while raw periodic reporting congests the random-access channel.")
fig(os.path.join(FIGDIR, "fig4a_task_capacity_agri.png"),
    "Figure 4. Task capacity (irrigation, 6 h deadline): supported devices per beam at 95% "
    "deadline success; semantic supports 1,600 versus 50 for raw periodic.")
fig(os.path.join(FIGDIR, "fig4b_task_capacity_env.png"),
    "Figure 5. Task capacity (flood warning, 45 min deadline): raw and compressed periodic "
    "reporting support zero devices at any modeled population; semantic supports 400.")
para("Under a correlated burst with 5% of devices active in one pass (M = 800), irrigation semantic "
     "reporting holds deadline success at 1.00. Flood-warning semantic reporting degrades from 0.93 "
     "to 0.75 and event-triggered from 0.96 to 0.81, while raw and compressed periodic remain at zero "
     "(Fig. 9). Correlated bursts partially reverse the average-traffic gain, as predicted in "
     "Section III.")
h2("C. Stage 3: Task Quality")
para("Table II reports episode-based task quality at the operating point of 100 devices per beam; a "
     "hit requires the decision to be delivered within the application deadline. For irrigation, "
     "semantic reporting achieves recall 1.000 \u00b1 0.000 with 0.06 \u00b1 0.07 false alarms per week "
     "and GTO = 19.6\u00d7. Decisions arrive 7.6 h early on average with 8.0 h mean timing error\u2014but "
     "so do all baselines (\u22125.1 to \u22127.9 h): the earliness is a property of the slow "
     "soil-moisture dry-down trace and the threshold rule, not of semantic reporting. For irrigation "
     "the asymmetry is benign (early irrigation is far cheaper than late), and it is reported as "
     "measured.")
para("For flood warnings, semantic reporting achieves recall 0.928 \u00b1 0.068 (miss probability "
     "0.072), 0.03 \u00b1 0.07 false alarms per week, and +0.51 h mean detection delay, giving "
     "GTO = 104.6\u00d7. The ratio is large because the raw baseline collapses (recall 0.157 \u00b1 "
     "0.111, miss probability 0.843) under the tight deadline; it is reported as measured, not "
     "trimmed. With ideal delivery the tuned rule has recall 1.0, so the residual 7.2% misses are "
     "access losses at 100 devices per beam, not decision errors. Event-triggered reporting reaches "
     "recall 0.657\u2014a respectable, cheap baseline; the semantic edge is the additional 27 points "
     "of recall plus 19\u00d7 less airtime. Figures 6\u20137.")
table("TABLE II. STAGE-3 TASK QUALITY AT 100 DEVICES/BEAM (EPISODE-BASED; HIT REQUIRES DELIVERY WITHIN DEADLINE)",
      ["App", "Mode", "Recall", "Pmiss", "FA/wk", "Delay", "GTO"],
      [["Agri", "raw", "1.000\u00b10.000", "0.000", "0.06\u00b10.07", "\u22125.1 h", "1.0"],
       ["Agri", "compr.", "1.000", "0.000", "0.06", "\u22125.9 h", "1.0"],
       ["Agri", "event", "1.000", "0.000", "0.09", "\u22127.9 h", "2.7"],
       ["Agri", "semantic", "1.000\u00b10.000", "0.000", "0.06\u00b10.07", "\u22127.6 h", "19.6"],
       ["Env", "raw", "0.157\u00b10.111", "0.843", "0.02", "+0.57 h", "1.0"],
       ["Env", "compr.", "0.206\u00b10.128", "0.794", "0.02", "+0.49 h", "1.5"],
       ["Env", "event", "0.657\u00b10.087", "0.343", "0.00", "+0.54 h", "83.5"],
       ["Env", "semantic", "0.928\u00b10.068", "0.072", "0.03\u00b10.07", "+0.51 h", "104.6"]])
fig(os.path.join(FIGDIR, "fig3a_quality_vs_resource_agri.png"),
    "Figure 6. Task quality versus radio resource (irrigation): semantic reporting matches raw "
    "recall (1.000) at 19.6\u00d7 less airtime; GTO = 19.6\u00d7.")
fig(os.path.join(FIGDIR, "fig3b_quality_vs_resource_env.png"),
    "Figure 7. Task quality versus radio resource (flood warning): semantic recall 0.928 versus "
    "0.157 for raw at 19.4\u00d7 less airtime; GTO = 104.6\u00d7 (large because the raw baseline collapses).")
h2("D. Energy")
para("Per device over 90 days at 100 devices per beam (Table III), semantic reporting consumes 286 J "
     "(agriculture) and 374 J (environment) versus 28,275 J and 28,310 J for raw periodic\u2014net "
     "savings of 99.0% and 98.7%. Raw-mode energy is dominated by access retries under congestion "
     "(about 25.8 kJ, the retry storm); semantic-mode energy is dominated by idle listening (117 J) "
     "plus sensing and inference. The 99% figure is load-dependent: at uncongested load the saving "
     "from fewer transmissions alone is about 95% (Fig. 8). Device-side intelligence remains "
     "beneficial for inference costs up to about 300 mJ (agriculture) and 100 mJ (environment) per "
     "decision\u2014orders of magnitude above the modeled 0.1\u20131 mJ and the 0.54\u20130.92 mJ "
     "hardware anchor [22]. All energy values are modeled, not measured on hardware.")
table("TABLE III. DEVICE ENERGY PER 90 DAYS AT 100 DEVICES/BEAM (MODELED NB-IOT-CLASS FIGURES)",
      ["App", "Raw", "Compr.", "Event", "Semantic", "Saving"],
      [["Agri", "28,275 J", "27,197 J", "1,566 J", "286 J", "99.0%"],
       ["Env", "28,310 J", "27,240 J", "291 J", "374 J", "98.7%"]])
fig(os.path.join(FIGDIR, "fig5_energy.png"),
    "Figure 8. Device energy per 90 days at 100 devices/beam: raw energy is dominated by access "
    "retries under congestion; semantic saves 99.0% (agriculture) and 98.7% (environment). Modeled figures.")
fig(os.path.join(FIGDIR, "fig6_burst.png"),
    "Figure 9. Correlated-burst robustness (5% of devices in one pass, 800 devices): irrigation "
    "semantic holds deadline success at 1.00; flood-warning semantic degrades 0.93 to 0.75.")
h2("E. Drift and Threshold Adaptation")
para("Thresholds tuned on dry-season data only were evaluated on monsoon segments. For flood warnings "
     "the stale threshold degrades to recall 0.746 with 0.88 false alarms per week (the tuner, seeing "
     "zero flood examples, degenerately selected the most conservative offset); a single downlink "
     "threshold update restores recall 1.000 with 0.08 false alarms per week, matching the oracle "
     "tuned on full-season data, at negligible downlink cost. Irrigation thresholds generalize across "
     "seasons (dry-tuned performance equals full-tuned). The guarded update loop of Section III-D "
     "exists because of this failure mode, not in spite of it.")

# ================================================================ VI
h1("VI. DISCUSSION AND FUTURE WORK")
para("Every gain in Section V is bounded to its named application, trace generator, task constraint, "
     "modeled energy figures, access configuration, and load range; no universal percentage for "
     "massive Internet of Things over NTN is claimed [10], [12].")
para("The following extensions are the natural next steps. First, validating the evaluation on field "
     "sensor datasets\u2014rainfall, soil-moisture, and river-level records\u2014beyond the calibrated "
     "synthetic traces used here. Second, sweeping multiple constellations and link configurations "
     "beyond the single configured sparse low-Earth-orbit scenario. Third, modeling NTN-specific "
     "random access (NB-IoT NPRACH) in place of the slotted-ALOHA abstraction, and measuring energy "
     "on MCU-class hardware with NTN chipsets to complement the modeled NB-IoT-class figures. "
     "Fourth, heterogeneous device/receiver decision rules, since the present gain measures where and "
     "when information is sent rather than model superiority. Finally, alternative deadline and "
     "reliability operating points beyond the 6 h / 45 min deadlines and the 0.95 success criterion "
     "assumed here.")
para("Smart metering, industrial monitoring, and asset tracking were part of an earlier "
     "five-application framing and are condensed here to future work: metering must retain exact "
     "values for billing while outage and anomaly functions can use compact decisions; industrial "
     "monitoring can replace waveforms with fault features under stringent missed-fault limits; asset "
     "tracking needs mobility-adaptive reporting. Each requires its own task operating point and "
     "baselines before any mixed-beam conclusion.")
para("Sustainability is reported as energy per successful task, including inference, signaling, "
     "retransmission, and model-update distribution\u2014not transmitter power alone; broader "
     "life-cycle claims require separate evidence.")

# ================================================================ VII
h1("VII. CONCLUSION")
para("This paper replaced an illustrative framework with measured evidence: a three-stage, "
     "trace-driven evaluation of task-oriented semantic reporting for massive Internet of Things over "
     "non-terrestrial networks, narrowed to irrigation decisions and flood warnings with an "
     "India-oriented lens. The measured offered-byte gain of 42.6\u00d7 decomposes into 18.9\u00d7 report "
     "suppression and 2.25\u00d7 payload shrinkage; supported devices per beam rise from 50 to 1,600 "
     "for irrigation, while periodic reporting cannot meet the flood-warning deadline at any modeled "
     "population; task-throughput-efficiency gains of 19.6\u00d7 and 104.6\u00d7 are achieved at matched "
     "or better task quality, with honest reporting of residual misses, timing error, "
     "congestion-amplified energy savings, and drift behavior. The results identify when semantic "
     "operation improves correct, timely task outcomes per unit of radio resource\u2014sparse, "
     "deadline-critical event traffic under constrained access\u2014and when raw-data fallback remains "
     "required. All claims are bounded to the evaluated applications, traces, models, and load "
     "ranges; the simulation package is released for independent reproduction.")

# ================================================================ REFERENCES
h1("REFERENCES")
refs = [
    '3GPP, “Study on Narrow-Band Internet of Things (NB-IoT)/enhanced Machine Type Communication (eMTC) support for Non-Terrestrial Networks (NTN),” TR 36.763, Rel. 17, 2021.',
    'ITU-R, “Framework and overall objectives of the future development of IMT for 2030 and beyond,” Recommendation ITU-R M.2160-0, Nov. 2023.',
    'ITU-R, “Future technology trends of terrestrial International Mobile Telecommunications systems towards 2030 and beyond,” Report ITU-R M.2516-0, Nov. 2022.',
    'E. C. Strinati and S. Barbarossa, “6G networks: Beyond Shannon towards semantic and goal-oriented communications,” Computer Networks, vol. 190, Art. no. 107930, May 2021.',
    'T. M. Getu, G. Kaddoum, and M. Bennis, “Making sense of meaning: A survey on metrics for semantic and goal-oriented communication,” IEEE Access, vol. 11, pp. 45456–45492, 2023.',
    'E. Delfani and N. Pappas, “Semantics-aware updates from remote energy harvesting devices to interconnected LEO satellites,” IEEE Communications Letters, vol. 29, no. 8, pp. 1928–1932, Aug. 2025.',
    'E. Delfani, A. Mesodiakaki, L. Tassiulas, and N. Pappas, “Semantics-aware unified terrestrial non-terrestrial 6G networks,” IEEE Communications Magazine, 2026, doi: 10.1109/MCOM.001.2500615.',
    'E. Zeydan, L. Blanco, C. J. Vaca-Rubio, M. Caus, and K. Dev, “Semantic non-terrestrial communications with Open RAN-enabled 6G,” IEEE Communications Standards Magazine, vol. 9, no. 4, pp. 72–78, Dec. 2025.',
    'L. X. Nguyen et al., “A contemporary survey on semantic communications: Theory of mind, generative AI, and deep joint source-channel coding,” IEEE Communications Surveys & Tutorials, vol. 28, 2026.',
    'D. Gündüz et al., “Beyond transmitting bits: Context, semantics, and task-oriented communications,” IEEE Journal on Selected Areas in Communications, vol. 41, no. 1, pp. 5–41, Jan. 2023.',
    'G. Xin, P. Fan, and K. B. Letaief, “Semantic communication: A survey of its theoretical development,” Entropy, vol. 26, no. 2, Art. 102, 2024.',
    'N. Tavakolian, H. Purmehdi, and J. Baek, “Rethinking communication metrics: How should we measure meaning?” arXiv:2608.21626, Aug. 2026.',
    'F. Chiariotti, A. Munari, L. Badia, and P. Popovski, “Goal-oriented medium access with distributed belief processing,” in Proc. IEEE INFOCOM, 2025.',
    'F. Minani et al., “QoSem-based resource allocation for semantic communication in NTN downlinks,” in Proc. IEEE GLOBECOM, 2024, pp. 2587–2592.',
    'F. Minani et al., “Resource allocation for semantic communication in NTN downlinks,” IEEE Transactions on Cognitive Communications and Networking, 2025, doi: 10.1109/TCCN.2025.3558006.',
    'H. Peng, Z. Zhang, Y. Liu, Z. Su, T. H. Luan, and N. Cheng, “Semantic communication in non-terrestrial networks: A future-ready paradigm,” IEEE Network, vol. 38, no. 4, pp. 119–127, Jul. 2024.',
    'P. Agheli, N. Pappas, and M. Kountouris, “Semantic filtering and source coding in distributed wireless monitoring systems,” IEEE Transactions on Communications, vol. 72, no. 6, pp. 3290–3304, Jun. 2024.',
    'V. Mannoni, V. Berg, S. Cazalens, and P. Raveneau, “System level evaluation for NB-IoT satellite communications,” in Proc. IEEE VTC2022-Spring, Helsinki, Jun. 2022, pp. 1–6.',
    'D. Richter, “Practical performance analysis of NB-IoT across terrestrial and non-terrestrial networks,” Bachelor’s thesis, 2026 (field measurements, not peer-reviewed).',
    'S. Górecki, S. Hausman, and P. Korbel, “Cross-layer energy management in embedded AIoT sensor networks: A structured review, full-cycle energy model, and break-even analysis,” Electronics, vol. 15, no. 17, Art. 4000, 2026.',
    'X. Chen, C. Huang, G. Chen, D. Feng, and P. Xiao, “The communication and computation trade-off in wireless semantic communications,” IEEE Wireless Communications Letters, vol. 14, no. 7, pp. 2259–2263, Jul. 2025.',
    'I. Lamaakal et al., “TinyHAR-UQ: Battery-aware, uncertainty-controlled tinyML for wearable activity recognition on IoT edge devices,” Internet of Things, vol. 36, Art. 101889, Mar. 2026.',
    'S. Kaul, R. Yates, and M. Gruteser, “Real-time status: How often should one update?” in Proc. IEEE INFOCOM, 2012, pp. 2731–2735.',
    'K. Taueatsoala et al., “TinyML-enabled IoT for sustainable precision irrigation,” arXiv:2601.13054 [cs.LG], Jan. 2026.',
    'V. Wiangnak, M. Wiboonrat, and S. Duangsuwan, “Development of an AIoT-based early flash-flood warning system for smart rural disaster resilience,” Sensors, vol. 26, no. 11, Art. 3512, Jun. 2026.',
    'K. J. Åström and B. Bernhardsson, “Comparison of Riemann and Lebesgue sampling for first order stochastic systems,” in Proc. IEEE CDC, 2002.',
]
for i, rt in enumerate(refs, start=1):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.left_indent = Pt(18)
    p.paragraph_format.first_line_indent = Pt(-12)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(f"[{i}] {rt}")
    r.font.size = Pt(8.5)
    r.font.name = "Times New Roman"

out = os.path.join(OUTDIR, "SPACOMM2027_TaskOriented_Semantic_mIoT_NTN.docx")
doc.save(out)
print("saved", out)

# ------------------------------------------------- citation audit
text = "\n".join(p.text for p in doc.paragraphs)
cited = sorted(set(int(m) for m in re.findall(r"\[(\d+)\]", text)))
print("cited in body:", cited)
print("n refs:", len(refs))
missing = [c for c in cited if c > len(refs)]
print("missing ref entries:", missing)
uncited = [i for i in range(1, len(refs) + 1) if i not in cited]
print("uncited refs:", uncited)
# check ascending first-appearance order
order = [int(m) for m in re.findall(r"\[(\d+)\]", text)]
seen = []
for n in order:
    if n not in seen:
        seen.append(n)
print("first-appearance order ok:", seen == sorted(seen), seen)
