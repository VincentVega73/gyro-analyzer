# Measurement methodology

## Optical tracking

Frames are processed locally. A marker is represented by observed image coordinates p = (x, y) and detection quality information. Official-target acquisition considers connected regions, contrast with white surroundings, compact shape, area and temporally consistent motion. Manual tracking can seed a dark or coloured mark. A predicted position guides visualization and association but is never substituted for a measured point.

## Geometric calibration and perspective

A stationary camera observes an approximately circular or elliptical trajectory. Robust spatial fitting rejects isolated outliers and requires broad angular coverage. A circle is preferred when an ellipse adds no justified improvement; otherwise an affine ellipse can correct moderate viewing tilt. Held-out spatial observations help compare models. General projective distortion, rolling shutter and lens distortion are not completely removed by this approximation.

Let c be the fitted centre, a and b the semi-axes and α the ellipse orientation. Rotate p − c into ellipse coordinates (u, v). The angular coordinate is:

```text
u =  (x − cx) cos α + (y − cy) sin α
v = −(x − cx) sin α + (y − cy) cos α
θ = atan2(v / b, u / a)
```

Calibration is checked against subsequent observed positions. In Precision measurement it is fixed. A changed scene is a validity problem, not an invitation to smooth the result until it looks stable.

## Phase reconstruction

Angles wrap modulo 2π. Consecutive trustworthy observations are unwrapped into continuous phase. When an interruption makes the number of intervening turns ambiguous, the record starts a new phase block. A global turn count is not invented across ambiguous gaps.

## Phase Regression

Within each coherent block j, the model is φᵢ = βⱼ + ωtᵢ + εᵢ, with a shared angular-speed slope and block-specific intercepts. Robust regression limits the influence of isolated outliers. Mean rotational speed is:

```text
RPMphase = 60 ω / (2π)
```

Uncertainty accounts for temporal dependence using block-based estimates rather than treating every frame as independent. Model assumptions and effective observation duration still limit interpretation.

## Revolution Timing

Full-turn crossings are interpolated from observed phase. For N complete turns over elapsed time Δt:

```text
RPMturn = 60 N / Δt
```

Only supported, coherent crossings contribute. Segmented records and short records may have insufficient complete turns for a reliable estimate.

## Agreement, quality and limitations

The methods share camera frames, timestamps and geometry. They are algorithmically different but not independent physical references. Agreement detects some inconsistencies; it does not remove shared systematic error. Quality also depends on spatial residuals, angular coverage, losses, timing checks, drift and calibration validation. A detector confidence score is a heuristic, not a calibrated probability of accuracy.

Camera timestamps provide elapsed time. Dropped frames can be handled when correspondence remains unambiguous, but frame loss, motion blur, exposure changes and clock errors can still bias or invalidate results. No fit is constrained to the nominal speed. Consult [accuracy and uncertainty](accuracy-and-uncertainty.md) before drawing metrological conclusions.
