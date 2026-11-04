# Privacy and data processing

Status: technical disclosure for the 1.0 Stage 1 development build. It is not yet a finalized Google Play privacy policy. The legal operator and approved contact channel must be supplied before store publication.

## Camera

Camera permission is used to observe the rotating marker. Frames are processed on the device. Ordinary measurement stores numeric observations and diagnostics rather than a video. Optional diagnostic recording, disabled by default, can save up to 120 YUV frames into a local ZIP; these may contain the camera scene.

## Stored data

Session CSV/JSON, timing and camera configuration, device model, timestamps and any experiment comments are stored in app-private storage. There is no registration or cloud account. Clear storage in Android settings or uninstall the app to remove its private records. Backup is disabled in the audited configuration.

## Export and external apps

When you choose Export or Save PDF, Android's file picker writes to your selected provider. That provider may be a cloud service selected by you. PDF preview/printing passes the chosen target to your viewer or print service through Android. Website/support links open an external browser; the destination has its own privacy practices. Exported files remain at their destination after uninstall and must be deleted there. Review records and diagnostic images before sharing them.

## Network and third-party components

The audited build declares Camera permission and no INTERNET permission. Its dependencies are AndroidX/Jetpack components; no advertising, analytics or cloud-upload SDK is declared. There is no embedded telemetry/upload path in the reviewed application. Android, camera vendors, document providers, printers and browsers operate under their own policies; this statement does not cover their independent behaviour.

## Diagnostics and support

Diagnostic files are shared only when you export and submit them. Public GitHub reports are public: do not include personal or confidential information. Security concerns should use private vulnerability reporting if enabled; see [Security](../SECURITY.md). A finalized legal owner/contact and store Data Safety declaration remain release blockers.
