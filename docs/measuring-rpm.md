# Measuring RPM

1. Prepare and calibrate the target using the [calibration guide](automatic-calibration.md).
2. In Settings, select the nominal speed (33⅓ or 45 RPM). This affects deviation display; it does not force measured speed toward that value.
3. Prefer Precision measurement and a stable interval of 180–300 seconds. The default is 180 seconds. Longer duration cannot repair invalid geometry or a systematically wrong camera clock.
4. Return to Measure and tap Start measurement when enabled. A disabled start means readiness checks have not passed; open Calibration and follow its status.
5. Keep the setup unchanged. Do not touch the mount, platter or paper while recording. The app stores measurements rather than ordinary video; optional diagnostic frames must be enabled separately.
6. Tap Finish measurement to stop early, or wait for the configured duration. The report is saved automatically. Camera interruption or calibration failure can terminate a session; read its quality and technical status before using it.
7. Open History to review, compare or export. Exports use Android's document picker and require no broad storage permission.

For repeatability, use a series such as five 300-second sessions without changing the setup. Start each separately, record conditions and inspect every quality warning. A series can reveal variability or drift but cannot establish absolute accuracy without an external reference.
