# Accuracy and uncertainty

## Distinct quantities

| Quantity | Meaning | What it does not establish |
| --- | --- | --- |
| Resolution | Smallest displayed increment | Error bound |
| Statistical uncertainty | Variability supported by observations and model | All systematic errors |
| Repeatability | Dispersion under nominally repeated conditions | Traceability or absolute accuracy |
| Between-session variability | Changes between repeated sessions | A specific mechanical cause |
| Systematic error | Persistent bias from clock, optics or procedure | Detectability through repetition alone |
| Absolute accuracy | Closeness to a suitable reference value | Proven by extra decimal places |

The measured quantity is average rotational speed over a supported interval. A 95% statistical interval is conditional on the model and the uncertainty procedure. It is not a certified coverage claim for total measurement error.

## Shared errors

Agreement between two computational methods does not establish absolute measurement accuracy. Both use the same camera clock, detected positions and geometric calibration. Camera timestamp agreement checks internal consistency; it is not calibration of the timebase against an independent clock.

Moderate tilt can be approximated by an affine ellipse, while severe perspective, lens distortion and rolling shutter can remain. Poor centring, paper slip, moving mounts, blur and asymmetric thresholding can produce error. Print scale is not used to convert distance into RPM, but it influences recognition and geometry quality.

## External-reference procedure

1. Identify the phone, Android/app version, camera mode, target version, printer, lighting and mounting arrangement.
2. Select an independent reference with documented uncertainty and timing characteristics. Do not call another calculation from the same video independent.
3. Compare simultaneous or appropriately synchronized stable intervals at 33⅓ and 45 RPM. Account for real platter drift between intervals.
4. Repeat at least five adequately long sessions per condition. Report every exclusion and its reason; do not discard poor results just because they disagree.
5. Report mean difference, standard deviation, between-session range, duration, sample count and reference uncertainty. Examine dependence on camera tilt, exposure and frame rate.
6. Separate repeatability from estimated bias. Publish the complete conditions and limitations, and retain raw evidence privately with permission.

There are currently no completed, independently referenced physical accuracy results for this target standard. Synthetic ground truth tests establish software behaviour under the generated conditions only. No certified or traceable absolute accuracy specification is claimed.
