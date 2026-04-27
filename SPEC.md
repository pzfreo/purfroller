# Purfling Roller — Design Specification

## Purpose

A small roller device to compress laminated wood purfling strips from their as-made thickness (up to 2.5mm) down to a target thickness (minimum ~1.3mm). Inspired by a pasta roller / mangle.

## Material

- Purfling: laminated wood sandwich, 3mm wide, 1.3–2.5mm thick
- All printed parts: nylon (P1S printer)
- Axles: 6mm steel rod

## Design Overview

Two 25mm diameter smooth rollers. The upper roller is fixed and driven by a hand crank. The lower roller is carried in an inverted U-frame (crossbar at bottom, arms extending upward, open-topped axle slots) that slides vertically inside the main frame. Two M6 adjustment bolts thread up through the bottom crossbar of the main frame and bear on the underside of the U-frame crossbar, pushing it upward to close the gap. Gravity returns the U-frame when bolts are backed off. The device sits on a short stand to give access to the thumbwheels from below.

## Parts List

### Main Frame
- **2× side plates** — nylon, ~8mm thick. Each has:
  - Upper axle hole (fixed) near the top
  - Rectangular vertical slot in the lower portion to guide the U-frame arms (~3mm taller than arm length)
  - M3 heat set inserts in top and bottom edges for crossbar attachment
- **Bottom crossbar** — nylon, spans both side plates. Carries 2× M6 heat set inserts for adjustment bolts. M3 clearance holes each end.
- **Top crossbar** — nylon, spans both side plates, retains upper axle. M3 clearance holes each end.

### Inverted U-Frame (lower moving assembly, single printed piece)
- Crossbar at the bottom (8mm tall) — adjustment bolt tips bear on the underside of this
- Two arms (7mm × 14mm cross-section, 25mm tall) extending upward that slide in the side plate slots
- Open-topped axle slots (6.2mm wide × 5mm deep) at the top of each arm to accept the lower axle (axle retained by side plate slot walls once assembled)
- Inside width between arms: 41mm

### Rollers
- **2× rollers** — nylon, 25mm diameter × 40mm wide, smooth surface, 6mm axle bore

### Axles
- **2× 6mm steel rod** sections

### Crank
- Nylon, single piece L-shape (arm + handle)
- D-bore hub to match a flat filed on the upper axle rod
- Fitted to the upper (fixed) axle

### Stand
- Simple nylon or printed frame, raises device ~20mm off bench to give finger access to thumbwheels from below

### Hardware
- 2× M6 threaded rod with nylon thumbwheels (glued) — adjustment bolts, threaded up through bottom crossbar
- 2× M6 heat set inserts (in bottom crossbar)
- M3 heat set inserts and M3 screws throughout for frame assembly

## Key Dimensions

| Item | Dimension |
|------|-----------|
| Roller diameter | 25mm |
| Roller width | 40mm |
| Axle diameter | 6mm |
| Side plate thickness | ~8mm |
| Overall device width | ~56mm (40mm roller + 2× 8mm side plates) |
| Adjustment travel | ~3mm |
| Required adjustment range | ~1.2mm (1.3–2.5mm purfling) |
| Stand height | ~20mm (clears thumbwheel thickness + finger access) |
| M6 bolt positions | Directly below U-frame arms |
| **U-frame inside width** | **41mm** (40mm roller + 0.5mm clearance each side) |
| **U-frame arm cross-section** | **7mm × 14mm** (7mm through side plate, 14mm front-to-back) |
| **U-frame arm height** | **25mm** (1.5× front-to-back width for stable guidance) |
| **U-frame crossbar height** | **8mm** |
| **U-frame overall height** | **33mm** (25mm arm + 8mm crossbar) |
| **Axle slot width** | **6.2mm** (6mm axle + 0.2mm clearance) |
| **Axle slot depth** | **5mm** |
| Side plate slot height | TBD — U-frame arm length + 3mm travel |
| Side plate height | TBD — derive from full vertical stack |

## Assembly Sequence

1. Install M6 heat set inserts in bottom crossbar
2. Thread M6 adjustment rods with thumbwheels up through bottom crossbar
3. Attach bottom crossbar to side plates with M3 screws
4. Slide U-frame arms into side plate slots from above
5. Drop lower roller and axle into U-frame arm slots from above
6. Attach top crossbar with M3 screws — retains upper axle
7. Attach crank to upper axle
8. Place assembled device on stand

## Notes

- Bolt tips should bear on flat pads on the U-frame crossbar directly below each arm to avoid point loading
- Plain bore nylon-on-steel bearing surfaces throughout — no bearings required at this load and speed
- Upper roller driven; lower roller spun by friction through the workpiece
- Purfling enters by hand, operator ensures straight entry — no infeed guide needed
- Several dimensions marked TBD must be derived from the U-frame arm geometry before finalising the side plate design
