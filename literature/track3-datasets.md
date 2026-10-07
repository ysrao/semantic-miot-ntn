# Track 3 — Open trace datasets for the NTN semantic-communication evaluation

Purpose: real, openly available sensor traces to drive the simulation in paper Sections V.D (smart agriculture, India lens: rainfall, humidity, temperature, soil moisture, irrigation decisions) and V.E (environmental monitoring, India lens: rainfall intensity, river/reservoir water level, flood warning).

**Verification rule followed:** every URL below was either opened directly with a page fetch or found verbatim in a fetched page. Anything not verifiable is in Section 2, not Section 1.

---

## Section 1 — RECOMMENDED datasets (verified downloadable)

### A. Smart agriculture candidates

#### A1. USDA NRCS SCAN — Soil Climate Analysis Network
- **Publisher/host:** USDA Natural Resources Conservation Service, National Water and Climate Center (NWCC)
- **Landing page:** https://www.wcc.nrcs.usda.gov/scan/ (fetched 2026-10-01 — program page live; hourly data for 200+ US sites)
- **Time span:** multi-decadal; pilot instituted 1991, most sites reporting 2000s–present (station-dependent)
- **Sampling interval:** hourly (all variables reported hourly)
- **Variables:** soil moisture and soil temperature at multiple depths (typically 2", 4", 8", 20", 40"), air temperature, relative humidity, precipitation, solar radiation, wind speed/direction, barometric pressure, snow depth/water equivalent
- **Geographic coverage:** United States (200+ sites; ~400 planned; 38 in Utah, many in agricultural states); Caribbean sub-network (Puerto Rico/USVI, 9 stations)
- **Number of sensor nodes:** >200 stations
- **Access terms:** fully open, no registration, no key. Public-domain US federal data. Hourly per-station CSV downloads from the NWCC site (station inventory at `http://www.wcc.nrcs.usda.gov/nwcc/inventory`, per-station hourly downloads documented in the community docs: https://ncss-tech.github.io/soilDB/reference/fetchSCAN.html and http://mesonet.agron.iastate.edu/scan/ — "Download Hourly data"; R package `soilDB::fetchSCAN()` also wraps it)
- **Suitability note:** best variable match for V.D of any verified source — soil moisture + rainfall + humidity + temperature at the paper's 5–15 min/15-min sensing cadence (hourly is close; can be interpolated or used at 1 h cadence). Caveats: US-only (not India, but crop-irrigation physics transfer; pair with A3/IMD for the India lens); hourly granularity misses sub-hourly irrigation dynamics; some stations have gaps after extreme events (e.g., Caribbean sites damaged by hurricanes Irma/Maria 2017); soil-moisture calibration is probe-type dependent (dielectric constant).

#### A2. ISMN — International Soil Moisture Network
- **Publisher/host:** TU Wien / Federal Institute of Hydrology (BfG), under WMO auspices
- **Landing page / data portal:** https://ismn.earth/en/data/data-download/ (fetched content 2026-10-01 — "You can access all data free of charge if you are registered with ISMN")
- **Time span:** network-dependent (earliest contributing networks ~1990s; ongoing)
- **Sampling interval:** network-dependent: sub-hourly / hourly / daily / intermittent (only a few times a month for legacy networks); check data-availability page per station
- **Variables:** soil moisture (m³/m³), soil suction, soil temperature, air/surface temperature, precipitation (mm), snow depth; static metadata: soil texture, bulk density, field capacity, wilting point
- **Geographic coverage:** global, densest in North America and Europe; includes the IITM (Indian Institute of Tropical Meteorology) network in India — the closest openly downloadable in-situ Indian soil-moisture trace
- **Number of sensor nodes:** thousands of stations across dozens of contributing networks (exact count varies per release; browse the portal)
- **Access terms:** free account registration required to download (viewing needs none); T&Cs require citing ISMN + networks. **Redistribution caveat:** ISMN terms forbid re-export/transfer of the original data to third parties — the revision's reproducibility package (Section VII.D) should ship scripts + trace identifiers and per-station file lists, not the data files themselves
- **Suitability note:** strongest India option for real soil-moisture traces (IITM network). Caveats: sampling intervals and record lengths are heterogeneous across networks, so the simulator must normalize cadence (e.g., resample to hourly); per-network QC flags differ; India coverage is sparse (handful of IITM sites) — use as the India validation holdout, train on denser networks

#### A3. IMD gridded daily rainfall (0.25°) + daily tmin/tmax (1.0°) — India
- **Publisher/host:** India Meteorological Department, Climate Monitoring and Prediction Group (CMPG), Pune
- **Landing pages:** rainfall — https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_Bin.html (fetched 2026-10-01: "New High Spatial Resolution (0.25×0.25 degree) Long Period (1901-2024) Daily Gridded Rainfall Data Set Over India", 135×129 grid, mm units); temperature — https://imdpune.gov.in/cmpg/Griddata/Max_1_Bin.html and https://imdpune.gov.in/cmpg/Griddata/Min_1_Bin.html (1.0° daily tmax/tmin 1951–present, 31×31 grid — found verbatim in a fetched page; also confirmed in the fetched imdpune.gov.in CMPG page "IMD High resolution 1.0×1.0 degree gridded daily temperature data (1951-2024)")
- **Time span:** rainfall 1901–present; temperature 1951–present; plus a real-time daily feed
- **Sampling interval:** daily
- **Variables:** daily rainfall (mm), daily max/min temperature (°C); missing cells coded -999.0
- **Geographic coverage:** India (6.5–38.5°N, 66.5–100°E)
- **Number of sensor nodes:** gridded product (not station traces); derived from up to ~6955 rain gauges (1901–2010 IMD4 product)
- **Access terms:** open download, no registration. The MIT-licensed `imdlib` Python package (https://github.com/iamsaswata/imdlib — fetched 2026-10-01) automates year-wise download/opening of `rain`/`tmin`/`tmax` via `imd.get_data()` / `imd.open_data()`; also usable via the IMD-Gridded-Data-Analyzer offline archive
- **Suitability note:** the India-lens forcing data (monsoon phases, dry vs normal vs heavy-rain stratification in V.D/V.E). Caveats: daily gridded ≠ IoT sensor traces — use it to (a) drive the irrigation/flood event schedule for the simulator, and (b) stratify results by dry/normal/heavy-rain/monsoon periods, exactly as V.D requires; it cannot stand in for sub-daily sensor dynamics — pair with A1/A2 (hourly) for the device-level trace. Real-time daily feed available for recent dates.

#### A4. East Kazakhstan regional agrometeorological network (2022–2025)
- **Publisher/host:** research team (Solnechnoe/Lugovoe/Sulusary stations), deposited on Zenodo
- **Landing/download page:** https://zenodo.org/records/19707421 (fetched 2026-10-01 — published 2026-04-23, CC-BY-4.0, one ZIP `EKR_Agrometeorology_2022_2025.zip`, 15.1 MB, Download link present)
- **Time span:** growing seasons (May–September) 2022–2025
- **Sampling interval:** WS "OCES-1": hourly (14,614 records, 65 variables); WS "OCES-2" and "Altyn Kazan": minute resolution (2025; ~200k records each, 49 variables); plus discrete field campaigns of volumetric soil moisture (every 10 cm to 1 m)
- **Variables:** air temperature and humidity at 200 cm, atmospheric pressure, precipitation, wind speed/direction; soil temperature and moisture down to 100 cm; field-measured VWC profiles at phenological stages
- **Geographic coverage:** East Kazakhstan (steppe/forest-steppe, Altai–Sayan), Dfb/Dfa climate, Chernozem soils — active agricultural lands
- **Number of sensor nodes:** 3 agrometeorological stations
- **Access terms:** CC-BY-4.0, no registration (Zenodo direct download), CSV format
- **Suitability note:** the finest-grained openly licensed real field trace found (minute/hourly multi-variable, incl. humidity and rainfall). Caveats: only 3 stations, 4 growing seasons, Kazakhstan not India — best used as a secondary trace for robustness checks of the irrigation-decision logic, not the India headline result; minute-resolution data may need aggregation to the paper's sensing cadence; soil-moisture profile is at a subset of depths.

### B. Environmental monitoring candidates

#### B1. GRDC-Caravan extension (daily river discharge, global)
- **Publisher/host:** Global Runoff Data Centre (BfG, WMO) + Google Research; released on Zenodo
- **Landing/download page:** https://zenodo.org/records/15349031 (fetched 2026-10-01 — Version 0.6, published 2026-05-06, CC-BY-4.0, direct download: `GRDC_Caravan_extension_csv.zip` 8.8 GB, `GRDC_Caravan_extension_nc.zip` 7.6 GB)
- **Time span:** 1950–2023
- **Sampling interval:** daily
- **Variables:** daily river discharge (m³/s) + per-catchment meteorological forcing from ERA5-Land (total precipitation, temperature, PET, etc.) + 211 static catchment attributes (area, elevation, land cover, climate indices)
- **Geographic coverage:** 5356 catchments across 25 countries worldwide (this is the openly licensed subset of GRDC; the classic GRDC portal holds more but under request-only terms — see Section 2)
- **Number of sensor nodes:** 5356 gauges
- **Access terms:** CC-BY-4.0 — freely downloadable, redistributable, no registration
- **Suitability note:** the long-record discharge trace for flood-warning event studies (event = discharge percentile/threshold exceedance; correlated monsoon bursts visible in the long record). Caveats: daily resolution misses flash-flood sub-daily dynamics — pair with B2 (15-min) for the burst analysis V.E requires; catchment-average forcing rather than in-situ co-located rainfall; check the attribute table for Indian catchments before claiming India coverage (India is not confirmed in the 25-country list — treat as global).

#### B2. USGS NWIS Water Services (streamflow + gage height, US)
- **Publisher/host:** US Geological Survey
- **Landing page:** https://waterservices.usgs.gov/ (fetched 2026-10-01 — "provides USGS water data in machine-readable formats via REST APIs"; instantaneous, daily, statistics, site-metadata services; no API key required for legacy endpoints)
- **Time span:** station-dependent; some records exceed 100 years
- **Sampling interval:** instantaneous values at ~15 min (recent ~120 days) and daily values (long history)
- **Variables:** discharge/streamflow (parameter 00060, ft³/s), gage height / water level (parameter 00065, ft), water temperature, groundwater levels, peak flows, rating curves
- **Geographic coverage:** United States (~8,000+ monitoring sites; global coverage not provided)
- **Number of sensor nodes:** thousands of active stream gauges
- **Access terms:** fully open, no registration, no key (legacy `waterservices.usgs.gov/nwis/iv|dv|site|stat` endpoints; USGS asks for reasonable request rates); US public domain
- **Suitability note:** the only verified sub-daily water-level trace in this track — gage-height (water level) series are directly the V.E environmental node variable (river/reservoir level), and 15-min resolution supports the correlated-burst NTN simulation. Caveats: US-only; 15-min instantaneous data is provisional for the most recent months and subject to revision (use approved daily values or flag provisional data in QC); flash-flood-prone western gauges have frequent sensor-outage gaps during extreme events — exactly the missed-detection cases the evaluation must report, not interpolate away.

---

## Section 2 — Looked promising, NOT actually accessible (do not waste time)

1. **India-WRIS / Central Water Commission river-gauge data (the India water-level source V.E wants).** An independent researcher's documented access attempt (2026-07-31, https://github.com/shakhoyat/ml-lab/blob/HEAD/flood-dataset/docs/india_wris_attempt.md — fetched): `https://indiawris.gov.in/wris/` times out at the TCP layer; `https://nwdp.nwic.gov.in/` (National Water Data Portal) returns only an HTML portal, not a data endpoint; API access requires institutional registration and border-basin data is classified. CWC FloodWatch/RSMS portals are visualization dashboards, not bulk downloads. → Use A3 (IMD) + B1/B2 instead; do not budget time here.
2. **GRDC classic data portal (grdc.bafg.de).** Daily discharge available only via an email request form (~24 h turnaround), non-commercial use only, redistribution prohibited. → Use the GRDC-Caravan Zenodo subset (B1, CC-BY-4.0) instead.
3. **IMD station-level (point) data.** Officially "supply of meteorological data" is on payment basis via IMD Data Supply Units / National Data Centre, Pune (http://mausam.imd.gov.in/newdelhi/docs/data-procedure.pdf — fetched). No open bulk download. → Use the IMD gridded products (A3) instead.
4. **DEEP FARM banana use-case sensor dataset (Zenodo 17831262, Dominican Republic).** Real IoT farm sensors (temp, humidity, dew point, soil-moisture channels, irradiance, wind) but files are **restricted** — access by request only. Record page: https://zenodo.org/records/17831262 (fetched 2026-10-01).
5. **Kaggle "IoT smart farm sensor log" CSVs.** Frequently synthetic or demo-grade: e.g., the agrismart-ai project bundles Kaggle IoT telemetry with unknown provenance, and public repos ship `generate_dataset.py` that creates *synthetic* soil-moisture/temp/humidity series labeled for irrigation demos. Real traces need provenance; none of the examined Kaggle smart-farm CSVs could be verified as raw sensor logs. Treat any Kaggle ag-IoT file as suspect until the uploader documents deployment, sensor type, and collection period.
6. **IMD AWS/ARG station telemetry via api.imd.gov.in.** Undocumented for public use; the only integrations found require institutional credentials / static-IP whitelisting (floodguard repo docs, fetched). Not a reproducible open source for the paper.

---

## Section 3 — Evaluation design notes for the top picks

### Agriculture: SCAN (A1) + IMD gridded (A3)

**Raw trace → simulator input.** Take one SCAN agricultural site (e.g., a mid-latitude cropland station) at hourly cadence for 2–3 full years: soil moisture at 5 cm (≈2"), rainfall (accumulated from hourly), relative humidity, air temperature. These are the four V.D sensing channels. The NTN baseline simulates conventional reporting at the paper's Table II cadence (e.g., every 15 min–1 h: downsample the hourly trace; or use hourly as the "routine agriculture" cadence directly). For the India lens, extract the IMD rainfall/tmax/tmin grid cells over a target district (e.g., a semi-arid district in Maharashtra or a Punjab cell) for the same calendar window, and use them to stratify SCAN traces into dry / normal-rainfall / heavy-rain / monsoon phases (V.D requires regime-separated results).

**What becomes the "event" (task outcome, per V.A/C).** Define an irrigation decision task on the trace: label each day/hour as `irrigate / defer / inspect` from a ground-truth agronomic rule computed on the full trace — e.g., 5-cm volumetric water content below a crop-specific deficit threshold AND cumulative rainfall in the trailing 48 h below 5 mm ⇒ irrigate; heavy rain (>20 mm/day on IMD/gauge data) ⇒ defer; moisture between wilting point and field capacity ⇒ defer. The semantic agent transmits only when its local rule fires a decision change or crosses a confidence band. Task loss = control error (water applied vs. optimal) + missed-stress events + false irrigation triggers; Stage 3 compares semantic vs raw-payload receiver-side inference (train both on the same held-out years, split by year/season per VII.C).

**Sampling the simulator needs.** Simulator sensing cadence: 15 min–1 h (SCAN hourly suffices; upsample by hold-last only if simulating 15-min devices, and report the interpolation). Event/decision reporting cadence: daily or on-change (irrigation decisions are naturally sparse → strong q). Regime stratification: ≥2 full years to cover dry/normal/monsoon. Fallback traffic: reserve a small raw-sample fraction (e.g., daily raw sample or on-demand) for calibration/drift, counted in the accounting stage.

**Preprocessing caveats.** (1) Align time zones (SCAN hourly in local standard; IMD daily is IST 08:30–08:30 accumulation) — align event windows, not raw timestamps. (2) SCAN precipitation is in inches, soil moisture in %VWC — convert to mm/m³·m⁻³. (3) Gap handling: drop or forward-fill short gaps; long gaps (station outages) must be excluded from task-accuracy scoring, not imputed, since a missed real stress event during an outage is a data artifact, not a scheme failure. (4) IMD daily gridded data is a proxy for district weather, not the station's rain — keep it as a regime label, never as the sensor channel.

### Environmental monitoring: GRDC-Caravan (B1) + USGS NWIS (B2)

**Raw trace → simulator input.** Use GRDC-Caravan daily discharge (1950–2023) for 5–20 catchments spanning wet/dry regimes as the long-record baseline for flood-warning evaluation: per-catchment time series + the bundled ERA5-Land precipitation forcing as the rainfall-intensity driver. Use USGS NWIS 15-min gage-height (00065) and discharge (00060) series for a small set of flash-flood-prone gauges (e.g., 3–5 sites) to supply the sub-daily dynamics and the geographically correlated burst analysis V.E mandates (pick gauges in the same basin/storm path).

**What becomes the "event".** Flood-warning task: define the warning state from the trace itself — e.g., discharge exceeding the site-specific 95th (warning) / 99th (danger) daily percentile, or gage-height rate-of-rise exceeding a threshold over 1 h. The semantic node transmits on threshold crossing with warning level + confidence + location; normal periods are suppressed to a heartbeat (6–24 h). Task metrics: detection probability/delay, false alarms per year, missed-event probability — with the paper's correlated-burst scenario simulated by synchronizing the 15-min NWIS traces across nearby gauges during a shared storm window. The receiver-side baseline uses the same thresholds on full raw data, so any missed event is attributable to the admission policy, not a weaker classifier (per VII.C).

**Sampling the simulator needs.** Long-record daily (GRDC-Caravan) for training thresholds, estimating event prevalence, and computing false-alarm rates over decades (rare-event statistics need volume). Sub-daily 15-min (NWIS) for the access simulation: correlated arrivals, access-success under burst load, detection delay in minutes. Stratify by regime: monsoon/long-normal periods for average traffic (high q benefit), plus extracted storm windows for peak-load analysis — the two must be reported separately (V.E).

**Preprocessing caveats.** (1) Do not smooth away extremes: keep provisional-vs-approved USGS flags; sensor dropouts during actual flood peaks are missed-detection contributors, not missing data to interpolate. (2) Daily discharge underestimates flash peaks — never use GRDC-Caravan alone for detection-delay claims; that's the NWIS role. (3) Gauge datum and rating-curve changes over decades (USGS) and regulation effects (GRDC-Caravan attributes) mean thresholds must be percentile-based per era, not absolute. (4) India check: confirm whether Indian catchments are in the GRDC-Caravan 25-country set before using it as an India-lens dataset; if absent, position B1 as the methodology validation and use IMD rainfall (A3) as the India event driver.
