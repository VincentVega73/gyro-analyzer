# Preparing the official target

## Standard and design

GYRO-TARGET-1.0 is a monochrome design: a white 180 mm paper circle, one 7.5 mm spindle opening and one solid black 12 mm circular mark whose centre is 65 mm from the opening centre. The owner requested black-and-white printer compatibility; this replaces the green marker in the initial design brief. Legacy coloured-marker tracking remains available manually.

The 12/180 diameter ratio produces a 12-pixel mark when the paper occupies 180 pixels across. The 65 mm offset provides a useful orbit radius while leaving 19 mm between the marker edge and the outer edge. These are engineering design choices validated synthetically, not proven printer-independent optima. The 7.5 mm opening is a starting cut size, not a universal spindle fit. Enlarge carefully if necessary; never force the paper or leave it buckled.

## Print and cut

1. Choose [A4](../targets/gyro-optical-target-a4.pdf) or [US Letter](../targets/gyro-optical-target-letter.pdf) to match your actual paper.
2. Use ordinary matte white paper. Select black-and-white printing and 100% / Actual size. Turn off Fit to Page, shrink-to-fit and borderless enlargement.
3. Check the 50 mm control line with a ruler. Accept 49.5–50.5 mm for the preparation check. A correct scale alone does not guarantee camera recognition.
4. Confirm the offset mark is solid and has a clean boundary. Streaks, holes in the toner, glossy paper and ink bleed can impair detection.
5. Cut along the outer circle and spindle-opening guide. Remove all printed instructions and the ruler from the working disc.
6. With the platter stopped, fit the paper flat. Keep it clear of the stylus and tonearm. Do not attach extra coloured stickers or add extra marks.

## Centre and eccentricity

The spindle opening locates the paper mechanically. The algorithm does not assume that printed centre is the true rotation centre: it estimates the centre from the observed mark's motion. Small paper eccentricity is permissible provided the complete trajectory remains visible and the paper does not slip or lift.

## Recognition failures

A mark below 12 pixels, defocus, low white-paper brightness, glare, heavy motion blur or several dark moving objects may prevent acquisition. Increase diffuse light, frame more closely and remove extraneous objects. A spindle hole is smaller and does not move on an orbit; it should not complete calibration. The detector checks shape, white surroundings, motion, geometry and later observations. A visually similar moving foreign mark can still be ambiguous; do not use the target as an identity code.

Physical inkjet and laser checks are pending. Follow [validation status](validation-status.md) and the [physical protocol](physical-test-protocol.md).
