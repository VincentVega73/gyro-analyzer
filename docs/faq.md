# Frequently asked questions

## Does the phone rotate with the platter?

No. Mount it above the platter. Only the paper target rotates.

## Can I use a black-and-white printer?

Yes, that is the intended GYRO-TARGET-1.0 design. Printer/device physical acceptance is still pending. Use the exact PDF, matte white paper and 100% scale.

## Why not a green marker?

The owner prioritized monochrome printing. The official design uses one black marker and temporal/geometric validation. Manual coloured-marker tracking remains available for older targets.

## Is a manually selected centre required?

Not for the official automatic mode. The rotation centre comes from motion, not from a tap on the printed hole. Manual controls remain a fallback.

## Does 60 FPS guarantee more accuracy than 30 FPS?

No. Timing quality, light, blur, geometry and delivered frames matter. Some devices cannot sustain the requested rate.

## Is the application measuring wow and flutter?

Stage 1 focuses on average RPM. It makes no standardized wow-and-flutter measurement claim.

## Why are two methods shown?

They provide an internal consistency check. They share the camera and clock, so agreement is not independent calibration.

## Is a narrow uncertainty interval an accuracy guarantee?

No. It is conditional statistical information. See [accuracy](accuracy-and-uncertainty.md).

## Are images uploaded?

The audited development build processes locally and has no INTERNET permission or embedded upload service. Optional diagnostic frame exports can contain images; destinations are chosen by you. See [privacy](privacy.md).

## Can I reuse calibration tomorrow?

The current version validates reuse in memory; it does not persist geometry across app restarts. Recalibrate after restart or any setup change.

## Where is Google Play?

The listing is not published. A real link will be added after release. There is no public APK/AAB here.

## Is this open-source software?

The Android source is private. Public documentation visibility does not grant an open-source licence. Licensing terms are pending owner approval.
