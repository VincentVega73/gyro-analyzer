# Privacy Policy

Effective date: 6 November 2026. Application: Gyro Analyzer. Responsible developer and contact: Sergey Kravchinskiy, [kraffts@gmail.com](mailto:kraffts@gmail.com).

## Camera and local processing

Camera permission is used to observe the rotating marker. Camera frames are processed on your device. Ordinary measurement stores numeric observations and diagnostics rather than video. Optional diagnostic frame recording is disabled by default; when enabled it can save up to 120 YUV frames in a local ZIP. Those images may contain the surrounding scene. You can deny or revoke Camera permission in Android settings; measurement then requires permission to be restored. Offline instructions and target PDFs do not need camera access.

## Data stored on your device

The app stores session CSV/JSON, numeric marker positions, camera/timing configuration, device model, timestamps and experiment comments in app-private storage. No account is required. The app does not automatically transmit these records to the developer and contains no advertising, analytics or cloud-upload SDK. The reviewed app does not request INTERNET permission. Records remain until you clear application storage or uninstall. Android backup is disabled. Files you export remain at their destination and must be deleted separately.

## Actions you choose

Export and Save PDF use Android's file picker to write to a destination you select. That destination may be a third-party cloud provider. Preview and print pass the selected target PDF to your viewer or print service. External documentation and support links open your browser. Those providers and websites have their own privacy policies. Review diagnostic images and comments before sharing them. Public GitHub issues and discussions are publicly visible.

## Support correspondence

If you contact [kraffts@gmail.com](mailto:kraffts@gmail.com) or submit an issue, the developer receives the information you choose to send, such as your email address, device details and attached diagnostics, to respond and investigate the report. Email is handled by the email provider; GitHub submissions are handled by GitHub. Please send only information necessary for your request. Support correspondence is retained while needed to resolve and follow up on the request, or where retention is required by law. Contact the same address to request access, correction or deletion of information you have submitted. Public submissions and provider-held data may also require action through the provider. The app itself has no server account to delete.

## Security and changes

Keep your device and exported files secure. No transmission or storage system is guaranteed to be completely secure. Do not post secrets or personal information in public reports; use [private security reporting](../SECURITY.md) for vulnerabilities. Changes to this policy will be published here with an updated effective date. This policy describes Gyro Analyzer 1.0.0 (com.gyroanalyzer.tachometer). Measurement validation is not metrological certification.

## Third-party components and Google Play distribution

The app uses AndroidX/Jetpack and Kotlin components for camera, user interface and local processing. It has no advertising, analytics or cloud-upload SDK. Google Play manages distribution and app signing; its automatic protection may verify installation/licensing through Google Play. Google Play, Android and device services operate under their own privacy policies. This is distinct from developer-operated collection of measurement records.
