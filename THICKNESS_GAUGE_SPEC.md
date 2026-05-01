# Magnetic Thickness Gauge — Design Specification

## Purpose

Measure material thickness in the range 1–5mm (instrument plates, purfling strips etc.) from one side only, without needing access to both faces simultaneously.

## Principle of Operation

A steel ball bearing is placed on the inside/reverse surface of the material. A magnet in the gauge housing attracts the ball through the material, holding it against the inside face. Multiple Hall effect sensors detect the perturbation of the magnetic field caused by the ball's presence. The ball centre is at a distance of (material thickness + ball radius) from the sensor reference plane. Once calibrated this gives a direct thickness reading.

Using multiple sensors arranged symmetrically around the magnet axis provides redundant field measurements, enabling auto-calibration, off-centre detection, and improved accuracy.

## Hardware

| Component | Part | Notes |
|-----------|------|-------|
| Microcontroller | Seeed XIAO ESP32S3 | Built-in LiPo charging, USB-C, 3.3V, 21×17mm |
| ADC | ADS1115 | 16-bit, I2C, 4 channels, avoids ESP32 ADC non-linearity |
| Hall sensors | DRV5055A1 (×3 or ×4) | Ratiometric linear output, SOT-23, hand-solderable |
| Magnet | N42 or N52 neodymium | Strong enough to hold ball through 5mm of wood |
| Ball bearing | 3–4mm steel | Small mass keeps magnetic holding force manageable |
| Display | Small OLED | Shows thickness reading |
| Battery | LiPo | Charged via USB-C on XIAO |
| Housing | 3D printed nylon | Cylindrical, flat reference face |

## Sensor Arrangement

Three or four DRV5055A1 sensors placed at equal angles around the magnet axis (120° for three, 90° for four). All sensors at the same radial distance from the axis and the same depth behind the reference face.

- **Three sensors** — simpler, gives full symmetry information, minimum component count
- **Four sensors** — easier geometry, 90° spacing, one extra redundant reading

The ADS1115 has four input channels — conveniently matches four sensors, or three sensors plus battery voltage monitoring.

## Calibration

1. **Baseline:** with ball removed, record each sensor's reading — this is the magnet-only field at each position
2. **Reference:** place gauge against a single known-thickness reference (e.g. a 2mm gauge block or known plate) with ball on reverse — record perturbed readings
3. **Offset correction:** sensors compared against each other to remove unit-to-unit variation
4. **Curve fit:** field perturbation vs distance follows approximately an inverse cube law — store a calibration curve (polynomial or lookup table) in firmware

A single reference thickness is sufficient for calibration if the curve shape is determined empirically during development.

## Off-Centre Detection

If the ball is not centred on the magnet axis, sensors on opposite sides will read asymmetrically. Firmware compares sensor readings:
- If readings converge within a threshold — ball is centred, measurement is valid
- If readings diverge — display alignment warning to user
- Optionally: mathematically correct for small off-centre offsets using the vector information

## Housing

- Cylindrical 3D printed nylon housing
- Flat reference face that rests on the outside material surface — this is the zero reference plane
- Magnet and sensors fixed at known geometry behind the reference face
- ADS1115 and wiring also within housing
- XIAO ESP32S3 and display at rear of housing
- LiPo battery within housing
- USB-C port accessible for charging

## Firmware Overview

- Read all Hall sensor channels via ADS1115 over I2C
- Subtract baseline (ball-absent) readings
- Check sensor symmetry — flag if off-centre
- Apply calibration curve to convert field reading to thickness
- Display thickness on OLED
- Battery state monitoring on spare ADS1115 channel (voltage divider on LiPo)

## Open Questions

- Exact magnet size and grade to be determined empirically — needs to hold ball reliably at 5mm through wood without saturating sensors
- Optimal radial and axial position of sensors relative to magnet — requires bench prototyping before finalising housing geometry
- Three vs four sensors — decide after prototyping
- Ball bearing diameter — 3mm or 4mm, depends on magnet strength achieved
