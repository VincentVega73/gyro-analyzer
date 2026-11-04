# Automatic calibration

## Normal workflow

Open Calibration, allow Camera and choose Calibrate automatically. Start the platter with the complete official target in view. No manual centre or marker selection is required in this mode.

Acquisition segments compact dark regions with a sufficiently bright surrounding ring. It also supports a broad green colour gate for legacy targets. Connected area, shape, size and temporal association filter candidates. A candidate must move on a sufficiently covered, stable circle or affine ellipse. The selected orbit is then fixed and checked against new observations before measurement readiness is enabled. No nominal RPM is supplied to acquisition.

The target is not recognized by a barcode or a single exact pixel value. A stationary spot, partial arc or multiple plausible moving candidates must not be treated as a successful lock. Predictions never count as observed marker points.

## Status and action

| Status | Meaning | Action |
| --- | --- | --- |
| Looking for target | Candidate motion is being collected | Keep rotating; hold the camera still |
| No suitable marker | No candidate passes image checks | Add diffuse light, improve focus or move closer |
| Several moving candidates | Identity is ambiguous | Remove other marks/objects |
| Not enough stable orbit coverage | Motion/fit is not yet sufficient | Continue rotating; reduce tilt or secure the mount |
| Orbit found; checking | New observations are validating geometry | Keep the setup unchanged |
| Ready to measure | Current observations support calibration | Start measurement |
| Orbit no longer matches | Setup changed or tracking became inconsistent | Stop and recalibrate |

## Timing and reuse

The target is readiness within 10 seconds in recommended conditions; this is an acceptance goal, not a proven device guarantee. Completion depends on observed geometry and its validation, not merely a countdown. The legacy manual path retains its existing readiness checks. In-memory reuse is validated with new observations after each session. Geometry is not persisted across a full application restart. Precision measurement fixes the accepted model; it does not quietly refit a moved scene into a trustworthy result.

Manual controls remain a fallback for nonstandard targets. Select the corresponding dark/colour mode in Settings, select the mark, and use trajectory-based centre acquisition. See [troubleshooting](troubleshooting.md).
