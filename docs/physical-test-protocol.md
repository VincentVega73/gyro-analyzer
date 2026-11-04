# Physical target acceptance protocol

Status: not executed. Synthetic image tests do not fulfil this protocol.

Use freshly printed GYRO-TARGET-1.0 PDFs, not a hand-drawn mark. Record target/PDF hash, paper format, printer and driver settings, measured 50 mm line, ink/toner quality, phone, Android/app versions, camera mode, actual FPS, exposure, mount, light, viewing angle, turntable, nominal speed and test date.

Test inkjet and monochrome laser printing (plus colour laser in monochrome mode where available), A4 and Letter, normal/bright/dim acceptable illumination, overhead/moderate tilt, 30/60 FPS where exposed, and ideally at least three phone models and several turntables. Record unavailable modes as unavailable, not passed.

For each condition perform independent cold acquisitions and repeated measurements. Start the acquisition timer when Calibrate automatically is pressed; stop at true measurement readiness. Record first-attempt success, elapsed time, all failure reasons, any false lock, centre/orbit evidence, tracking losses, method agreement, duration and reference comparison if available. Deliberately test multiple marks, stopped platter, moved camera, partial occlusion, print scaling errors and poor focus.

Before collecting data, agree a representative sample size and distribution. Suggested minimum: 100 recommended-condition acquisitions and 100 expanded-condition acquisitions, distributed across devices/printers; report confidence intervals alongside rates. Acceptance goals are at least 98% first-attempt success in recommended conditions, at least 95% in expanded conditions, at least 95% of successful recommended acquisitions ready within 10 seconds, and no undetected gross centre/phase errors. These percentages are targets, not current claims.

For RPM, compare repeated stable 33⅓ and 45 RPM runs with an independent reference if available. Record both methods and all quality exclusions. Any systematic target-version bias or false successful calibration blocks production release until investigated and retested.
