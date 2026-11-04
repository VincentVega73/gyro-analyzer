# Understanding results

RPM is revolutions per minute. Deviation is 100 × (measured RPM / nominal RPM − 1), expressed as a percentage. Duration and complete turns indicate the observation interval supporting the result.

Phase Regression estimates a common slope of phase versus time. Revolution Timing estimates speed from interpolated full-turn crossings. Their difference is an internal consistency check. See [methodology](measurement-methodology.md).

The displayed uncertainty is conditional statistical uncertainty, not a total error budget. Decimal places follow available uncertainty and quality; an unreliable result may be rounded more coarsely. Do not interpret a stable third decimal as certified absolute accuracy.

The report graph displays saved short-window RPM observations, with a dashed nominal reference. It does not fabricate data across invalid gaps. The vertical scale spans at least ±0.2 RPM around nominal and expands for data. Time-window selection changes the view, not the measured result.

Quality warnings include insufficient observations, inconsistent methods, drift and geometry no longer matching calibration. Do not hide these warnings by averaging sessions. In tracking loss, the live screen distinguishes the last observed estimate and its age from a current measurement. Previous saved values are available in History, not silently reused as live RPM.

CSV contains machine-readable measurements and validity fields. Technical JSON includes calibration, timing, quality and uncertainty details. CSV replay reprocesses exported coordinates; it cannot verify the original pixels or printer recognition.
