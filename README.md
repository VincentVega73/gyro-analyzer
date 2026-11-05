# Gyro Analyzer

Camera-based, contact-free measurement of average turntable rotational speed on Android.

## Project status

**In development: 1.0 Stage 1.** This repository is the public documentation and printable-target workspace. It does not contain the Android application source code. The first Google Play release is not yet available. No public APK/AAB is distributed here. Development version numbering previously reached UI 3.0; the product release line starts at 1.0, with monotonically increasing Android version codes.

The new monochrome target and automatic acquisition are under validation. Synthetic tests are not a substitute for printed-target tests on physical devices. Do not interpret the repository description as a certified accuracy claim.

## Overview

Gyro Analyzer observes a marker on a rotating platter while the phone remains on a stable mount. Unlike methods that put a phone on the platter and use its motion sensors, this optical method does not add the phone's mass to the rotating system. Lighting, camera geometry, image timestamps and print quality still matter.

## Implemented development-build features

- Contact-free optical marker tracking, including legacy coloured markers.
- Official monochrome target acquisition without tapping its centre or marker.
- Geometric calibration from observed motion, with circle or affine ellipse selection.
- Continuous phase reconstruction with separate blocks when lost cycles are ambiguous.
- Phase Regression and Revolution Timing estimates of average RPM.
- Quality warnings, conditional uncertainty and calibration validation.
- Measurement history, comparison, CSV and technical JSON export.
- Offline target PDFs, Android save/preview/print and an introductory guide.
- English, German, Spanish and Russian interface and offline instructions. English is the fallback for unsupported system languages.

## How it works

A single offset marker traces a closed orbit. The application estimates the orbit from positions, reconstructs phase and relates phase or complete-turn events to camera timestamps. The nominal speed is a comparison reference; it is not a fitting constraint. See [measurement methodology](docs/measurement-methodology.md).

## Quick start

1. Check [availability and system requirements](docs/getting-started.md). Google Play distribution is pending; there is no store link yet.
2. Download the [A4 target](targets/gyro-optical-target-a4.pdf) or [US Letter target](targets/gyro-optical-target-letter.pdf), and follow [printing instructions](docs/target-preparation.md).
3. Stop the platter, cut and place the paper flat as described in [target preparation](docs/target-preparation.md).
4. Mount the phone securely using [camera setup](docs/camera-setup.md).
5. Start rotation with the complete marker orbit visible.
6. Open Calibration and choose Calibrate automatically; follow [automatic calibration](docs/automatic-calibration.md).
7. When ready, start a [measurement](docs/measuring-rpm.md).
8. Review quality, [interpret results](docs/understanding-results.md) and export through the report.

## Measurement accuracy

Resolution is the displayed increment. Statistical uncertainty describes the fitted model and its assumptions. Repeatability describes dispersion under repeated conditions. Systematic error can affect every repetition. Absolute accuracy requires comparison with a suitable independent reference. Agreement between the two methods does not establish absolute accuracy: both share observations, geometry and a camera clock. Read [accuracy and uncertainty](docs/accuracy-and-uncertainty.md).

## Documentation

- [Documentation index](docs/index.md) and [verified publication evidence](docs/publication-evidence.md).
- Engineering papers: [Optical Measurement Methodology](docs/measurement-methodology.md) and [Accuracy, Uncertainty and Validation](docs/accuracy-and-uncertainty.md), verified against algorithm 2.2.1. Historical replay includes invalidated geometry; official-target physical acceptance remains pending.
- [Complete user guide](docs/user-guide.md) and [getting started](docs/getting-started.md).
- [Camera setup](docs/camera-setup.md), [target standard](targets/README.md) and [automatic calibration](docs/automatic-calibration.md).
- [Measuring RPM](docs/measuring-rpm.md), [results](docs/understanding-results.md), [methodology](docs/measurement-methodology.md) and [accuracy](docs/accuracy-and-uncertainty.md).
- [Troubleshooting](docs/troubleshooting.md), [FAQ](docs/faq.md), [compatibility](docs/compatibility.md), [privacy](docs/privacy.md) and [support](docs/support.md).
- [Roadmap](ROADMAP.md), [changelog](CHANGELOG.md) and [release checklist](docs/release-checklist.md).

## Downloads

Official design files: [A4](targets/gyro-optical-target-a4.pdf), [US Letter](targets/gyro-optical-target-letter.pdf). Both use GYRO-TARGET-1.0, a single black marker and the same physical geometry. Physical acceptance is pending; see the [validation status](docs/validation-status.md). A Google Play link will be added only after publication.

## Support and feedback

Use [Issues](https://github.com/VincentVega73/gyro-analyzer/issues) for reproducible defects and [Discussions](https://github.com/VincentVega73/gyro-analyzer/discussions) for questions, measurement methodology and device reports. Follow the [reporting guide](docs/support.md). Remove personal details and review exported camera images before posting.

## Licensing and affiliation

Copyright 2026 Sergey Kravchinskiy. Documentation and official target PDFs are licensed under CC BY 4.0. Branding, logos and visual identity retain all rights. The Android application and source code are proprietary and closed source; CC BY 4.0 does not apply to them. See [license scope and attribution](LICENSE.md). See [licensing status](docs/licensing-status.md). Gyro Analyzer is independent and is not an official product of Michell Engineering or any turntable manufacturer.
