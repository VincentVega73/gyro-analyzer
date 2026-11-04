# Compatibility

Minimum Android version: 8.0 (API 26). Target API: 36 in the audited Stage 1 build. A rear camera and Camera permission are required. CameraX uses the device Camera2 implementation; supported resolutions, focus/exposure locks and FPS differ by device. The app lists advertised modes but that does not prove sustainable delivered frame rate.

Start with 640 × 480 and an available 30 FPS mode. Higher rates are optional. High-speed capture advertised by a phone's stock camera may not be available through this application's analysis pipeline. Handheld compensated measurement is not supported.

| Device/environment | Status | Evidence and scope |
| --- | --- | --- |
| Android 15 x86_64 emulator | Tested for UI only | Local UI 3.0 baseline screenshots and Stage 1 checks; simulated camera is not a physical turntable test |
| Physical Android devices with GYRO-TARGET-1.0 | Not Tested | Printer/device acceptance protocol is pending |

Community reports should identify device, Android/app versions, actual camera configuration, target version and reproducible results. Such entries are labelled Community Reported until reproduced. Known Issue entries must link to a concrete issue. Specification sheets alone do not establish compatibility.
