# Accuracy, Uncertainty and Validation

**Baseline:** application `1.0.0-stage1b` (version code 10), algorithm `2.2.1`; verified 2026-11-05. This paper distinguishes fresh numerical tests, historical recordings and experiments still required. See [methodology](measurement-methodology.md) for estimators and [evidence](publication-evidence.md) for conditions and outputs.

## 1. Terminology

| Term | Meaning here |
| --- | --- |
| Resolution | Smallest displayed or stored increment, not an error bound |
| Precision | Dispersion under specified conditions |
| Repeatability | Precision under substantially unchanged procedure and conditions |
| Reproducibility | Precision when declared conditions, such as device or operator, change |
| Random error | Unpredictable observation-to-observation variation |
| Systematic error | Persistent or predictably varying bias, such as clock scale |
| Statistical uncertainty | Estimated variation conditional on a statistical model |
| Confidence interval | A procedure with stated repeated-sampling coverage under assumptions |
| Absolute accuracy | Closeness to a reference, not established by internal agreement |
| Calibration | Establishing a relationship to reference values with uncertainties |

Storing 33.522927 RPM does not imply micro-RPM accuracy. A fitted-slope interval is conditional on data, geometry and timebase, not automatically a whole-instrument uncertainty budget. See [JCGM publications](https://www.bipm.org/en/committees/jc/jcgm/publications) and [NIST terminology](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-d1-terminology).

## 2. Error sources

| Source | Mechanism | Evidence and limitation |
| --- | --- | --- |
| Timestamps | Random jitter; systematic clock-scale bias | Simulations completed; physical clock calibration absent |
| Localization | Centroid noise and photometric bias | Coordinate-noise tests; real bias budget absent |
| Geometry | Wrong centre/axes cause periodic phase distortion | Synthetic tests and historical invalidations; no complete perspective/lens budget |
| Frame loss | Reduced coverage and unknown lost cycles | Drop simulations; no universal device tolerance |
| Phase | Incorrect turn count corrupts timing | Discontinuity checks; ambiguous blocks excluded |
| Regression | Constant-speed model, outlier influence and sampling bias | Numerical tests; arbitrary motion not covered |
| Drift | Genuine speed changes during the window | Replay drift indications; physical cause not isolated from optical errors |
| Target | Warp, contrast, shadows and eccentric mounting | PDF and image tests; printing acceptance pending |
| Camera | Exposure, resolution, stabilization, rolling shutter | Metadata audit; device-specific systematic budget absent |

![Error evidence map](figures/error-sources.svg)

*Figure 8. Qualitative evidence status, not a quantified uncertainty budget.*

Unmeasured terms must not be assigned zero. A physical uncertainty budget needs statistical and other evaluated contributions; see [NIST uncertainty basics](https://physics.nist.gov/cuu/Uncertainty/basic.html).

## 3. Phase uncertainty implementation

The robust phase fit is described in the methodology. Uncertainty takes the larger of two variance estimates rather than treating each video frame as an independent experiment.

Eligible non-overlapping five-second blocks provide ordinary-least-squares slopes, each requiring at least 12 observations and 3.5 s span. For m block RPMs, centred values z_j and L = min(m−1, ceil(m^(1/4))):

```text
M = Σ z_j² + 2 Σ[l=1..L] (1−l/(L+1)) max(0, Σ z_j z_(j−l))
SE_blocks = sqrt(M / (m(m−1)))
```

Negative lag covariance is clipped to zero. This is a conservative HAC-style modification, not a guarantee that all correlation is captured.

One-second clusters also accumulate slope scores S_c = Σ w_i x_i e_i, with block-centred time x_i, residual e_i and Sxx = Σ w_i x_i²:

```text
SE_clusters = sqrt(Σ S_c²) / Sxx × 60/(2π)
U95_phase = max(10⁻¹⁰ RPM, t95(m) × max(SE_blocks, SE_clusters))
```

`t95` is the implementation's conservative grouped Student lookup indexed by block count, not an exact continuously evaluated quantile. Fewer than two blocks yields no interval; reliable-window status needs at least three blocks, adequate duration/coverage and bounded residuals. Block count is a correlation safeguard, not a measured count of independent physical trials. Longer correlation and nonstationarity remain limitations.

The nominal 95% half-width is conditional on this model. The numerical floor is not a physical accuracy floor. A short window may yield an RPM before it supports meaningful uncertainty; missing uncertainty must not be displayed as zero.

## 4. Revolution Timing uncertainty

With interpolation fraction f and local rate v = |Δθ/Δt|, phase-noise propagation is:

```text
σ_t = sqrt(((1−f)σ_a)² + (f σ_b)²) / v
```

This assumes locally linear phase. It does not include calibrated clock uncertainty, every exposure effect or arbitrary acceleration error.

The robust time-versus-index regression uses within-group centred indices. Its HAC variance accumulates weighted index-residual scores with triangular weights through ceil(N^(1/4)) lags, excluding cross-group pairs. Unlike the phase block formula, signed lag contributions are retained. Final variance is floored at zero and at propagated crossing variance Σ x_k² σ_tk² / Sxx². For period standard error SE_T:

```text
U95_revolution = t_multiplier × 60 × SE_T / T_hat²
```

The helper receives N−G (events minus eligible groups), uses that argument minus one for its conservative Student lookup and requires N−G ≥ 5. Shared observations, geometry and clock errors correlate crossings. More turns constrain the period, but do not calibrate it. Very narrow synthetic intervals can simply reflect missing systematic terms in a simulator.

## 5. Agreement and drift

The difference is Revolution Timing minus Phase Regression. Phase comparison uses supported crossing intervals. Comparison blocks default to 30 s and require at least 90% span. At least three paired blocks support the 99% paired-difference limit, using triangular lag weights and non-negative covariance contributions. Drift assessment uses leverage-adjusted slope scores, a HAC term and an ordinary-regression variance floor.

Invalid geometry, inadequate coverage, ambiguous phase, drift or common bias can defeat the interpretation of agreement. A fresh simulation with true 33.52 RPM and elapsed timestamps multiplied by 1.0005 gives **33.503248376 RPM in both methods**. Their difference is below 10⁻¹⁰ RPM while both have about −0.016752 RPM error. Agreement does not independently verify the camera clock.

## 6. Fresh synthetic validation

Unchanged production measurement and tracking classes were compiled into a private command-line harness. These are fresh tests of algorithm 2.2.1, not a claim that every historical suite was rerun. Private source hashes, seeds and outputs are retained; [aggregate evidence](publication-evidence.md) is public.

| Family | Input | Duration / repetitions | Check |
| --- | --- | --- | --- |
| Ideal phase | 33⅓/45 RPM, 30/60/120 FPS, both directions | 65 s / 12 | Both errors below 10⁻⁸ RPM |
| Noisy phase | 33.52 RPM, 60 FPS, 0.01 rad Gaussian noise, ±1.5 ms uniform jitter, 20% periodic loss | 300 s / 12 seeds | Both errors below 0.01 RPM |
| Coordinates | 33.52 RPM, 110 × 75 px ellipse, 1 px Gaussian noise, initial centre displaced (30,20) px, jitter and 20% loss | 300 s / 5 seeds | Both errors below 0.01 RPM |
| Clock scale | 33.52 RPM, scale 1.0005 | 120 s / 1 | Both follow biased timebase |
| Official PDF images | Normal, tilt, dim, blur, loss, occlusion | 8 s / 7 positive cases | Acquisition and RPM checks pass |
| Negative acquisition | Stationary mark, competing marker, moving camera | 8 s / 3 | No accepted lock |

![Synthetic errors](figures/synthetic-errors.svg)

*Figure 9. Actual fresh harness outputs, RPM error relative to simulator truth. No physical instrument error is measured here.*

Official-target images are 640 × 480 at 30 FPS, generated from the actual A4 PDF. Positive locks occur at 3–5 s; maximum absolute RPM error is 0.000869 RPM. Every accepted tracked position meets the harness position check. This is a small deterministic simulation family, not a universal printer/device guarantee. Five or twelve trials do not establish universal interval coverage.

## 7. Historical Michell Gyro SE records

The collection is associated with experimental coloured-marker development. Per-file target identity, original app build, lighting, warm-up and independent reference are not fully recorded. Timestamp monotonicity does not calibrate clock scale. Records C, A and B contain CameraX timing metadata. Replay uses the stationary-camera path; actual mount stability is not independently established.

| Reference | Stored algorithm | Full duration | Current phase / revolution RPM | Current final status |
| --- | --- | --- | --- | --- |
| C, f1162eb0… | 2.1.0 | 243.307 s | 33.522946 / 33.522723 | UNRELIABLE, geometry invalidated |
| A, 4bde60ca… | 2.2.0 | 180.005 s | 33.487358 / 33.487270 | UNRELIABLE, geometry invalidated |
| B, b16e103f… | 2.2.0 | 94.254 s | 33.500580 / 33.501310 | UNRELIABLE, geometry invalidated |

![Historical replay](figures/real-comparison.svg)

*Figure 10. Real CSV replay with algorithm 2.2.1. All three records are invalidated; this is not an accepted-speed or before/after adjustment plot.*

Computed phase/revolution 95% half-widths are C: 0.008754/0.001964, A: 0.011692/0.001116, B: 0.016180/0.001401 RPM. These are **diagnostic outputs of invalidated records**, not valid platter uncertainty statements. Rejection supersedes the interval. Stored and replayed outputs differ with algorithm, finalization and comparison intervals.

The requested history mentions approximately 33.50 RPM before mechanical adjustment and 33.30 RPM after. No verified 33.30 RPM counterpart or file-to-adjustment mapping was found among seven unique supplied recordings. A quantitative adjustment effect is therefore **not established here**. The records demonstrate processing, consistency and calibration-failure detection, not a verified before/after change or absolute accuracy. Add the comparison only after identifying its data and procedure. Raw private CSVs are not published.

## 8. Proposed repeatability protocol

This five-run, five-minute protocol is a future experiment, not a completed result.

1. Record phone, OS, app/algorithm version, target version and PDF checksum. Print at actual size, measure the ruler and document mounting and flatness.
2. Fix the camera rigidly. Keep the orbit visible with modest tilt, uniform non-flickering light and no moving shadows. Record requested and delivered camera settings.
3. Use a declared, repeatable warm-up interval appropriate to manufacturer guidance. Log room conditions, belt/motor state and elapsed warm-up; keep conditions consistent.
4. Calibrate and wait for verified geometry. Record 300 s. Export CSV and technical JSON, preserving warnings, timing metadata and calibration state.
5. Repeat five times without speed adjustment. Declare whether calibration is retained or repeated and use one rule. Log gaps and interventions. Retain failed runs and justify exclusions.
6. For accepted run means R_i, report mean ΣR_i/5, sample standard deviation sqrt(Σ(R_i−Rbar)²/4), range and run order. If independent stationary runs are justified, a mean interval uses t_(0.975,4) s/√5. Check drift before applying it.

Variation includes real turntable drift and measurement variability. Five runs do not prove universal reliability. Different phones, operators, days and mounting angles constitute a separate reproducibility study.

## 9. Independent reference validation

Use an independently calibrated tachometer with documented status, range, resolution and uncertainty. Observe the same interval where practical; verify that its marker or loading does not affect the platter. Report differences and combined uncertainty, including covariance where relevant. Another estimator on the same camera is not independent.

A 3150 Hz test record supplies another chain: R_audio = R_ref × f_measured/f_ref. Its actual recorded frequency, eccentricity, warping, playback conditions, ADC clock, frequency estimator, analysis window and resampling matter. A nominal 3150 Hz label is not an exact standard. Evaluate the record and recording chain before assigning uncertainty. No calibrated audio-reference comparison is claimed here.

## 10. Official target status

| Layer | Status | Scope |
| --- | --- | --- |
| PDF geometry, metadata, checksums | PASS | Distributed design matches GYRO-TARGET-1.0 |
| Current PDF rendered-image tests | PASS: 7 positive, 3 negative | Limited synthetic detector compatibility |
| Physical monochrome printing | PENDING | No documented printer/stock acceptance series |
| Real-device automatic calibration on official print | PENDING | Coloured-marker records do not substitute |
| Independent absolute-speed comparison | PENDING | No traceable absolute accuracy claim |

## 11. Claims and recommendations

| Claim | Assessment | Required further evidence |
| --- | --- | --- |
| Ideal simulated RPM is recovered | Supported for tested conditions | Broader tests for broader claims |
| Official PDF geometry is correct | Supported | Physical print measurement |
| Noise and loss can be tolerated | Partially supported | Device/environment matrix |
| Records prove a 33.50-to-33.30 adjustment | Unsupported by available mapping/data | Identified before/after records and procedure |
| Agreement establishes absolute accuracy | Unsupported | Independent reference and uncertainty budget |
| Official target is physically accepted | Unsupported, pending | Printed-target/device protocol |
| Certified or traceably calibrated accuracy | Prohibited claim without evidence | Appropriate calibration and documented traceability |

Use fixed mounting, clean contrast, modest tilt, sufficient duration and actual timestamps. Inspect quality and drift before quoting digits. Recalibrate after movement; preserve rejected data for diagnosis. Report conditions and algorithm version. No particular physical accuracy level is promised.

## References

- [Methodology](measurement-methodology.md), [evidence](publication-evidence.md), [physical protocol](physical-test-protocol.md), [validation status](validation-status.md) and [index](index.md).
- [JCGM publications](https://www.bipm.org/en/committees/jc/jcgm/publications).
- [NIST uncertainty basics](https://physics.nist.gov/cuu/Uncertainty/basic.html) and [terminology](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-d1-terminology).

Copyright 2026 Sergey Kravchinskiy. Documentation and original explanatory figures: CC BY 4.0. Branding remains all rights reserved; Android application/source remain proprietary. See [license scope](../LICENSE.md).
