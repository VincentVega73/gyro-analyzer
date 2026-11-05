# Optical Measurement Methodology

Gyro Analyzer measures average rotational speed by observing one marker on a turntable with a stationary Android phone. It measures the relationship between orbital position and camera time, without putting the phone on the platter. This paper describes the inspected development implementation, not a certified instrument.

**Baseline:** application `1.0.0-stage1b`, version code 10; algorithm `2.2.1`; verification 2026-11-05. Historical CSV algorithm identifiers differ. Conditions and numerical outputs are recorded in [validation evidence](publication-evidence.md). The Android implementation remains proprietary.

## 1. Scope and system

Average RPM helps reveal sustained speed offset and monitor adjustment. Wow and flutter concern speed variation over specified frequency bands and require appropriate sampling, filtering and reference procedures. A precise average does not demonstrate low wow and flutter. No standardized wow-and-flutter measurement is claimed here.

![Measurement system](figures/measurement-system.svg)

*Figure 1. Original conceptual system diagram; no experimental data.*

The platter carries a target. The camera supplies images and timestamps. Detection produces image coordinates, calibration maps coordinates to phase, and estimators relate phase to time. Quality checks can invalidate a number even when arithmetic produces it. Nominal 33⅓ or 45 RPM is a comparison reference, not a fitting constraint.

## 2. Official optical target

The [A4 PDF](../targets/gyro-optical-target-a4.pdf) and [Letter PDF](../targets/gyro-optical-target-letter.pdf) implement **GYRO-TARGET-1.0**. Actual vector paths, page dimensions, metadata and checksums were checked.

| Feature | Design dimension | Meaning |
| --- | --- | --- |
| Working disc | 180 mm diameter | Fits A4 and Letter |
| Black marker | 12 mm diameter | One marker on white paper |
| Marker offset | 65 mm | Centre-to-centre distance |
| Spindle-hole guide | 7.5 mm diameter | Initial cutting guide, not universal spindle-fit approval |
| Control line | 50 mm | Measure after printing at actual size |

![Target dimensions](figures/target-geometry.svg)

*Figure 2. Design schematic in millimetres; not a printable target.*

Print at 100%, disable fit-to-page, measure the control line and use opaque flat paper. The preparation guide's 1% print-scale criterion is not an RPM accuracy claim. Uniform scale does not directly set RPM because the calculation uses angle rather than linear distance. Distortion, curling, shadows, eccentric mounting and spindle interference can nevertheless impair observation or rotation. Stop the platter before installation; see [target preparation](target-preparation.md).

One marker avoids ambiguous multiple passages per turn. The printed centre locates the intended mounting hole; the actual centre of rotation is estimated from motion. They need not coincide. Historical experimental green-marker recordings do **not** physically validate the official black-marker design. Physical acceptance remains **PENDING**.

See [versions](../targets/versions.json) and [SHA-256 checksums](../targets/SHA256SUMS.txt). Modified targets have not passed official compatibility validation unless separately documented. The Official Gyro Optical Target designation is not an absolute-accuracy certification.

## 3. Camera acquisition and timing

CameraX supplies YUV 420 888 images with keep-only-latest backpressure. Current defaults request 640 × 480 and 60 FPS. Requests are negotiation inputs, not delivery guarantees. Supported ordinary capture ranges determine selection; a dedicated high-speed YUV path is not implemented. Selecting 120 FPS does not establish 120 delivered or processed observations per second.

Capture FPS describes actual exposures; processed FPS describes frames reaching analysis. Backpressure can discard frames and tracking can reject others. The measurement uses `ImageInfo.timestamp` in nanoseconds. The timestamp origin is subtracted before conversion to floating-point seconds. Time is never frame number divided by nominal FPS.

The audit checks non-negative, strictly increasing timestamps and, where available, matching capture metadata, exposure, frame duration and rolling-shutter metadata. Missing metadata leaves the timebase uncalibrated. Arrival time is operational monitoring information, not the measurement clock.

Android specifies sensor time as the exposure start of the first sensor row. No calibrated midpoint-exposure or row-dependent rolling-shutter correction is applied. Constant offset changes an intercept; varying exposure or row timing can change phase and slope. Stabilization is requested off, which alone does not prove device behaviour. See [CameraX analysis](https://developer.android.com/media/camera/camerax/analyze) and [sensor timestamp](https://developer.android.com/reference/android/hardware/camera2/CaptureResult#SENSOR_TIMESTAMP).

## 4. Detection and tracking

Automatic acquisition operates directly on YUV planes, segmenting dark regions with support for legacy green regions. Four-connected components are screened by size, shape, fill and surrounding brightness. Candidate tracks are associated by movement and area. Acceptance requires orbital motion, plausible geometry and repeated stable fits with high heuristic confidence. Competing moving candidates prevent acceptance; a stationary black spot is insufficient.

Manual tracking can learn a small selected image patch, then use chroma or dark-intensity matching. Region-of-interest segmentation identifies components; a full-resolution weighted centroid estimates position. Area, elongation, ambiguity and photometric tests affect confidence. Confidence is a heuristic score, **not a calibrated probability**.

Prediction helps locate the next candidate but is never treated as an observed coordinate. Loss reduces coverage. Recovered observations must pass geometry and phase checks; unknown whole turns are not fabricated to fill a gap. Automatic acquisition removes small tap targets from setup, not the need for contrast and a fixed camera.

## 5. Circle and affine ellipse calibration

A circular orbit viewed obliquely generally appears elliptical. The implementation uses a centred algebraic circle solution within deterministic RANSAC, residual refinement and angular-coverage checks. An ellipse candidate uses a normalized conic fit, robust sampling and held-out comparison with the circle. Minimum point counts, axes, inlier fraction, angular distribution and normalized residuals are checked. Solving a conic through a few points is insufficient.

Ellipse selection requires substantial held-out residual improvement and a compatible centre. Geometry changes need repeated consistent proposals. Independent off-orbit observations can invalidate accepted calibration; lack of observations leaves it unverified. Moving the camera requires recalibration. Geometric residuals do not measure camera-clock accuracy.

![Circle and ellipse](figures/circle-ellipse.svg)

*Figure 3. Synthetic image geometry in pixels.*

For image point (x,y), centre (cx,cy), semiaxes a,b and orientation φ:

```text
u = ((x − cx) cos φ + (y − cy) sin φ) / a
v = (−(x − cx) sin φ + (y − cy) cos φ) / b
θ = atan2(v,u)                            [rad]
```

A circle has a = b. `ELLIPSE_AFFINE` is affine normalization, **not complete projective camera calibration**, lens calibration or a camera-pose solution. Strong perspective and lens distortion may leave systematic errors.

![Centre error](figures/centre-error.svg)

*Figure 4. Synthetic unit-circle example: centre displaced by 0.1 radius produces periodic phase error despite constant physical speed.*

## 6. Phase reconstruction

Wrapped angle covers one revolution. Unwrapping selects a nearby continuation using recent phase motion. Within a continuous block:

```text
θ(t) = θ0 + ωt + ε(t)
```

θ0 is phase origin; ω is angular speed in rad/s; ε includes localization, geometry error and real departures from constant speed. Gaps longer than two seconds or ambiguous continuations start new blocks. Global phase is not asserted across unknown lost turns. Regression gives separate intercepts to discontinuous blocks; crossing epochs likewise avoid inventing inter-block revolution counts.

![Phase continuity](figures/phase-continuity.svg)

*Figure 5. Synthetic example in seconds and radians. Missing observations do not establish a turn count across the gap.*

## 7. Phase Regression

Fits use observed timestamps and accepted coordinates. Low confidence, excessive blur, inadequate light, off-orbit motion and handheld operation can reject observations or invalidate quality. Nonuniform sampling is represented by actual time values.

Let x_i and y_i be time and phase after subtraction of their weighted means within each continuity block:

```text
ω_hat = Σ w_i x_i y_i / Σ w_i x_i²
RPM_phase = |ω_hat| × 60 / (2π)
```

Three iteratively reweighted passes use residual scale max(0.0005 rad, 1.4826 × median absolute residual) and weights min(1, 2.5 × scale / max(10⁻¹², |residual|)). This is robust reweighting, not ordinary least squares relabelled as robust. It reduces outlier influence but cannot remove shared systematic error.

A numerical fit needs 12 observations and two seconds. Reliable-window status also requires adequate duration, coverage, residual control and at least three eligible uncertainty blocks. Computability alone is insufficient; see [uncertainty](accuracy-and-uncertainty.md).

![Phase regression](figures/phase-regression.svg)

*Figure 6. Synthetic explanatory phase observations and linear trend; not an additional application benchmark.*

## 8. Revolution Timing

The second estimator locates integer multiples of 2π in the rotation direction. For adjacent observations bracketing θk:

```text
f = (θk − θa) / (θb − θa)
tk = ta + f (tb − ta)                     [s; stored as rounded ns]
```

Crossings require the same continuity block, compatible direction and positive elapsed time no greater than 0.25 s. Gaps and implausible jumps reset epochs. Both directions are supported; RPM is a non-negative magnitude. Unknown turns across epochs are not counted.

The endpoint diagnostic is 60N/(tN−t0), with N supported complete turns. The primary estimator instead fits:

```text
tk = α_group + k T + error_k
RPM_revolution = 60 / T_hat
```

Groups have separate intercepts and a common positive period. Eligible groups need three events and there must be at least four overall. Four robust passes reduce crossing-time outlier influence. Interrupted data contribute supported within-group timing, not fictitious bridges. Endpoint and fitted-period results need not coincide.

![Crossing interpolation](figures/revolution-timing.svg)

*Figure 7. Synthetic crossing neighbourhood. Sub-frame interpolation assumes locally linear phase; it does not improve absolute clock calibration.*

## 9. Estimator agreement

Phase Regression uses many angles; Revolution Timing uses supported complete-turn events. Comparison restricts phase fitting to supported crossing intervals. Paired block differences and an autocorrelation-aware 99% limit assess consistency. Drift, invalid geometry, insufficient blocks or disagreement override a numerical match.

Both methods share timestamps, coordinates, geometry and phase. They are mathematically distinct but statistically dependent. **Agreement is a consistency check, not absolute calibration.** A common clock-scale error can bias both almost identically.

## 10. Worked examples

### Ideal simulated rotation

At 33⅓ RPM, ω = 10π/9 = 3.490658504 rad/s and T = 1.8 s. At 60 observations/s the ideal phase increment is 0.058177642 rad. Sixty turns span 108 s: 60 × 60/108 = 33.333333333 RPM. Phase conversion 60ω/(2π) agrees. Twelve implementation tests cover 33⅓/45 RPM, 30/60/120 FPS and both directions over 65 s; both estimators satisfy a 10⁻⁸ RPM numerical tolerance. This validates arithmetic, not physical accuracy.

### Real historical recording, with rejected calibration

Reference C, SHA-256 `f1162eb0093cfbc75d65390cc98e4cccc37ffd5be7c2d97d6d6bbc27da4fe2ae`, has 13,366 rows over 243.306987 s. Its stored algorithm is 2.1.0; original app build is absent. It is from the experimental-marker collection, not official-target acceptance. Per-file target identity and environment were not independently recorded.

At elapsed 9.050253 s an accepted observation was (512.179268, 297.502568) px. The final reported ellipse has centre (385.154307, 307.460692) px, axes (128.926142, 127.094023) px and orientation 1.524318470 rad. Substitution gives u = −0.031379573, v = −1.002017634 and atan2(v,u) = −1.602102484 rad. The online phase was −0.073389851 rad, using geometry available then. Final analysis reprojects history as geometry changes; this approximately quarter-turn origin difference illustrates why intermediate values must retain their geometry version rather than mixing online and final coordinates.

On supported comparison intervals, current algorithm 2.2.1 gives ω = 3.510514745181 rad/s and 33.522946470 RPM. Crossing regression gives T = 1.789830757022 s and 33.522722618 RPM from 131 events and 130 supported turns. Endpoint timing gives 33.521865381 RPM over 232.683949 s.

Final status is **UNRELIABLE / GEOMETRY_INVALIDATED**, with a drift indication. A small difference of −0.000223852 RPM does not restore validity. Computed intervals are diagnostic, not a validated measurement uncertainty. This example demonstrates both the calculation and its rejection status.

## 11. Limitations and references

Clock scale, rolling shutter, varying exposure, marker bias, affine-model limitations, printing, lighting and blur can produce systematic error. Lost frames reduce evidence and can make phase ambiguous. Real drift violates a constant-speed model. Longer records reduce some statistical effects but do not cancel all biases.

Average-speed estimation and internal diagnostics are demonstrated under stated conditions. Certified or traceably calibrated absolute accuracy is not established. Continue with [accuracy and uncertainty](accuracy-and-uncertainty.md), [numerical evidence](publication-evidence.md), [physical protocol](physical-test-protocol.md) and [documentation index](index.md).

Copyright 2026 Sergey Kravchinskiy. Documentation and original explanatory figures: CC BY 4.0. Branding remains all rights reserved; Android application and source code remain proprietary. See [license scope](../LICENSE.md).
