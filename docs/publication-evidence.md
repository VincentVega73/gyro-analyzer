# Publication Evidence — GYRO-106

Verified 2026-11-05 against application 1.0.0-stage1b / algorithm 2.2.1. These tables are generated from fresh private harness results. No raw recordings or Android source are distributed. Original explanatory diagrams are CC BY 4.0, copyright 2026 Sergey Kravchinskiy.

## Reproducibility boundary

The private harness compiles unchanged measurement and tracking classes with Kotlin 2.2.10 and runs deterministic inputs. Source and input hashes, scripts and full output remain in the private audit package. Public aggregate [JSON](publication-results.json) supports independent table and figure recalculation, but does not make the proprietary algorithm publicly rerunnable. Units: RPM; durations: seconds. Historical timestamps were checked strictly increasing; eight files contained seven unique byte streams. Original app build and per-file physical target identity are unavailable, so historical outputs are diagnostic evidence only.

## Numerical trials

| Family | Trials | Phase RPM range | Revolution RPM range | Maximum absolute error, either method |
| --- | --- | --- | --- | --- |
| ideal | 12 | 33.333333333–45.000000000 | 33.333333333–45.000000000 | 1.953992523e-11 |
| noise | 12 | 33.519983025–33.520013596 | 33.519932169–33.520072262 | 7.226169652e-05 |
| coordinate | 5 | 33.519981438–33.520003465 | 33.519859383–33.520125278 | 0.000140616757 |

Ideal: 65 s, 33⅓ and 45 RPM, 30/60/120 FPS, both directions. Noise: 300 s, 33.52 RPM, 60 FPS, seeds 1–12, 0.01 rad Gaussian phase noise, uniform ±1.5 ms jitter, every fifth observation dropped. Coordinates: seeds 21–25, 300 s, 33.52 RPM, 60 FPS, ellipse semiaxes 110/75 px, 1 px Gaussian noise, initial centre displaced by (30,20) px, same jitter and periodic loss. Acceptance thresholds are described in [accuracy](accuracy-and-uncertainty.md).

## Current official PDF image tests

Source A4 SHA-256: `ce259c3c94213d8359953410e5908907dbc9aa1ab07d3953aff5182f7013f1dc`. Source Letter SHA-256: `23e563d80854379e8b99ae77c1e8422b5c5a5c4a74c73c7ca735c38137dc04d5`. The Letter PDF receives structural checks; image sequences use A4.

Frames: 640 × 480, 30 FPS, 8 s; 241 frames before omissions; image noise seed 401. Tilt uses vertical scale 0.75; dim uses scale 0.85, brightness 0.72 and 3-level noise; blur uses scale 0.9, 1-level noise and Gaussian blur 1.2 px. Drop omits every eleventh frame at remainder 5; occlusion hides five frames per 60. Negative cases are stationary, a competing opposite marker, and sinusoidal camera translation.

| Case | Truth RPM | Lock time s | Recovered RPM | Outcome |
| --- | --- | --- | --- | --- |
| normal33 | 33.333333 | 3 | 33.33311858552365 | pass |
| normal45 | 45.000000 | 3 | 45.000059652487614 | pass |
| tilt33 | 33.333333 | 5 | 33.333629455709435 | pass |
| dim45 | 45.000000 | 5 | 45.00064952524115 | pass |
| blur33 | 33.333333 | 5 | 33.332464484297766 | pass |
| drop45 | 45.000000 | 3.533333333 | 45.00007317089568 | pass |
| occlusion33 | 33.333333 | 3.5 | 33.333178520972744 | pass |
| stationary | 0.000000 | — | — | rejected as required |
| two_markers | 33.333333 | — | — | rejected as required |
| camera_move | 33.333333 | — | — | rejected as required |

These are simulated images of the actual PDF, not photographs of printed targets. Physical acceptance remains PENDING.

## Historical identity

| Reference | SHA-256 | Stored algorithm | Current final result |
| --- | --- | --- | --- |
| C | `f1162eb0093cfbc75d65390cc98e4cccc37ffd5be7c2d97d6d6bbc27da4fe2ae` | 2.1.0 | UNRELIABLE / GEOMETRY_INVALIDATED |
| A | `4bde60ca93732dde584b8cf60e473fdf940b8eef90b0e3e5a7f4acd6dd4f6d14` | 2.2.0 | UNRELIABLE / GEOMETRY_INVALIDATED |
| B | `b16e103f67ad0616d9cf0cc5cfce6c8d4e8348b569aac5884492d5906cd9c0f1` | 2.2.0 | UNRELIABLE / GEOMETRY_INVALIDATED |

The task author identifies the development collection with the Michell Gyro SE and experimental coloured markers. The files alone do not independently prove mounting, lighting, target identity or before/after adjustment order. Only requested derived aggregates are published. No verified 33.30 RPM counterpart was identified.

## Reading the results

See [methodology](measurement-methodology.md), [accuracy and uncertainty](accuracy-and-uncertainty.md) and [documentation index](index.md). No physical absolute accuracy is certified by these tests.
