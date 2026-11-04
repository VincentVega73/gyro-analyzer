# User guide

GYRO ANALYZER 1.0 STAGE 1

Purpose and requirements
Measure average turntable rotational speed with a stationary phone camera. Android 8 or later and a rear camera are required. This is a development build, not a certified instrument. No account or connection is needed for measurement. Keep the tonearm away from the paper.

1. Prepare the target
Open Help, then Prepare target. Select A4 or US Letter. Preview opens your PDF viewer; Save PDF uses Android’s file picker; Print opens Android’s print service. If no viewer or printer service is installed, save the PDF and print it on another device. The same PDFs are bundled offline. Use matte white paper and black-and-white printing. Print at 100% / Actual size, never Fit to Page. Check the 50 mm line with a ruler (49.5–50.5 mm). The circle is 180 mm across, the offset black marker 12 mm across at a 65 mm radius, and the spindle opening 7.5 mm. Cut the outer circle and centre opening; remove the text and ruler outside the circle. Never force a tight spindle opening; enlarge it only as needed for a flat fit.

2. Install and position
Stop the platter before handling the target. Place it flat, clear of the stylus and tonearm; do not hold the phone on the platter. Mount the phone securely above it. Show the complete white circle and use diffuse, steady light. Avoid shadows, reflections and additional dark spots. At 640 × 480, aim for a circle at least 180 pixels wide and a marker at least 12 pixels wide. Start rotation only after your hands are clear. Do not move the phone during calibration or measurement.

3. Calibrate automatically
Tap Set up camera or Calibration and allow camera access. Tap Calibrate automatically. No centre or marker tap is needed for the official target. The app checks compact dark objects against their white surroundings, follows actual motion, fits a circle or affine ellipse and checks new observations. A stationary spot cannot complete calibration. Multiple moving candidates prevent acceptance. Wait for Ready to measure, then Start measurement. If a failure persists, follow the displayed guidance: add light, move closer, remove other marks, reduce the viewing angle or secure the mount. Manual controls retain centre/marker selection for unusual or older coloured targets; choose Dark marker or Coloured marker in Settings as appropriate.

4. Measure
Choose 33⅓ or 45 RPM in Settings to set the reference, not to constrain the estimate. Precision measurement locks geometry. The default interval is 180 s. Longer stable records generally provide better statistical information than short ones. Tap Finish measurement to stop early. Loss of tracking shows the last observation with its age; predicted positions are not measurements. Moving the phone or stopping the camera interrupts recording. Recalibrate after changing camera mode or position. Reuse is validated only within the current process; restarting the app requires calibration.

5. Read and export
The result shows RPM, deviation from nominal, duration, full revolutions, Phase regression, Revolution timing and uncertainty. A warning or unreliable result overrides extra decimal places. History opens saved sessions and can compare two sessions. In the report, scroll to the real recorded RPM graph, time window and Export. Choose CSV or JSON and a writable destination. CSV uses fixed machine-readable decimal points regardless of interface language. Diagnostic frame recording is optional, off by default and adds processing load; its ZIP can contain camera images. Review every export before sharing.

6. Troubleshooting
Permission denied: enable Camera in Android app settings and reopen calibration. No camera: close other camera apps and restart the preview. Unsupported FPS: select a listed lower rate, typically 30, and recalibrate; requested FPS may differ from delivered FPS. Marker missing: check print scale, contrast, focus, illumination and a complete orbit in view. Multiple candidates: remove marks or objects from the scene. No stable orbit: confirm the platter rotates and the phone does not move. Different estimates: inspect tracking and geometry, increase duration and repeat; do not average an unreliable result into a good one. Export failure: select another writable location. Saved values appear only in History/results, never as a new live reading.

7. Accuracy, privacy and help
Displayed resolution, statistical uncertainty, repeatability and absolute accuracy are different quantities. Two agreeing methods share the same camera, geometry and clock; agreement is not external calibration. High FPS alone does not guarantee accuracy. Compare repeated long measurements with an independent reference before making absolute accuracy claims. Physical compatibility of the new printed target remains under validation. Camera frames are processed locally. Results stay in app-private storage; clearing app storage or uninstalling removes them. Files exported through Android remain at the chosen destination and must be deleted there. There are no advertising SDKs, accounts or embedded telemetry in this build. Help can reopen this guide and the first-run wizard. English, German, Spanish and Russian are available in Settings; unsupported system languages fall back to English.

## Related guides

[Target preparation](target-preparation.md) · [FAQ](faq.md) · [Troubleshooting](troubleshooting.md) · [Measurement limitations](accuracy-and-uncertainty.md)
