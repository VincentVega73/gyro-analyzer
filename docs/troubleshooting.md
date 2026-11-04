# Troubleshooting

| Symptom | Likely causes | Actions | Escalate when |
| --- | --- | --- | --- |
| Camera permission denied | Permission not granted | Enable Camera in Android app settings; reopen Calibration | Permission is granted but preview remains unavailable |
| Camera unavailable | Another app owns camera; device/API failure | Close other camera apps; restart preview and app | Reproducible on an otherwise working rear camera |
| Unsupported frame rate | Device does not expose requested mode | Choose a listed lower FPS; recalibrate; inspect delivered FPS | Advertised mode consistently fails with details recorded |
| Marker not detected | Small image, blur, low light, weak contrast, bad print | Check 50 mm scale, solid black ink, focus, diffuse light and ≥12 px mark | Correct target and clear frames still fail |
| Multiple candidates | Extra dark objects or marks | Remove extra marks; keep one complete target visible | A single clean target still reports ambiguity |
| Calibration never completes | Incomplete orbit, camera movement, severe perspective | Start rotation, secure mount, reduce tilt, show full orbit | Stable complete orbit fails repeatedly |
| Insufficient lighting | Paper too dark, long exposure | Add diffuse light and reduce noise | Adequate light still yields failures |
| Excessive reflections | Glossy paper or direct lamp | Use matte paper and redirect/diffuse light | Reflections persist across reasonable setups |
| Tracking lost | Occlusion, sudden movement or identity ambiguity | Remove obstruction, stop invalid session and recalibrate | Repeated losses occur in clear view |
| Inconsistent RPM estimates | Geometry error, short record, drift or ambiguous gaps | Inspect warnings; extend duration; repeat stable tests | Long valid sessions still disagree |
| Insufficient duration | Too few supported observations or complete turns | Record a longer stable interval | Warning remains in long uninterrupted records |
| CSV export failed | Unwritable destination or provider failure | Select another folder; check storage space | Local writable destinations also fail |
| Previous result appears stale | A saved report is open or tracking was lost | Check screen title and last-observation age; return to Measure | A saved result is shown as a new live observation |
| PDF will not open | No installed viewer | Save PDF and open with a viewer/on another device | Saved PDF is corrupt or unreadable |
| Incorrect print dimensions | Scaling or paper mismatch | Match A4/Letter; use 100%; disable fitting | Control line remains wrong at actual size |
| Device gets hot | High FPS, diagnostics or long use | Stop, allow cooling; lower FPS; disable frame diagnostics | Severe heating recurs under normal use |

For each report include reproducible steps, app/Android versions, device, camera settings and target version. Avoid posting personal information or unreviewed diagnostic frames. See [support](support.md).
