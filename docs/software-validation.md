# Stage 1 software validation

Candidate: 1.0.0-stage1, version code 9. Full suite: 73 tests, zero failures/errors. Debug APK, release AAB and Android Lint completed successfully. Release signing and Google Play submission are not complete.

The 12 baseline tracking/calculation source files are byte-for-byte unchanged. Automatic acquisition is a new component integrated through the existing model and calibration guard.

Ten synthetic cases rendered from the delivered PDF geometry cover 33 1/3 and 45 RPM, affine tilt, dim/noisy illumination, blur, dropped frames, brief occlusion, stationary input, competing markers and camera movement. Seven rotating valid cases acquired; three rejection cases did not lock. See [numeric results](synthetic-validation.json). ViewModel readiness was 6.033333333 seconds in the normal synthetic case; recording and target-version metadata were verified.

These are deterministic 640x480, 30 FPS synthetic sequences, not physical acceptance measurements. They do not establish phone compatibility, real printer tolerances, extreme perspective performance, 60 FPS operation, thermal stability or absolute accuracy. The licensed PDF revision only adds footer/author notices outside the working disc; the tested geometry is unchanged.

Four language resource sets and offline manuals are checked by automated tests. Complete visual, physical device and print validation remains a release gate. See [physical protocol](physical-test-protocol.md).
