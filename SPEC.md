# Purfling Roller — Design Specification

## Purpose

A small roller device to compress laminated wood purfling strips from their as-made thickness (up to 2.5mm) down to a target thickness (minimum ~1.3mm). Inspired by a pasta roller / mangle.

## Material

- Purfling: laminated wood sandwich, 3mm wide, 1.3–2.5mm thick
- All printed parts: nylon (P1S printer)
- Axles: 6mm steel rod

## Design Overview

Two 25mm diameter smooth rollers, one fixed (lower) and one adjustable (upper), driven by a hand crank. The upper roller is carried in a U-frame that slides vertically inside the main frame. Two M6 adjustment bolts push the U-frame and upper roller down toward the lower roller to set the gap.

## Parts List

### Main Frame (lower assembly)
- **2× side plates** — nylon, ~8mm thick. Each has:
  - Lower axle hole near the bottom
  - Rectangular cutout in the upper portion to guide the U-frame arms
  - M3 heat set inserts in top and bottom edges for crossbar attachment
- **Bottom crossbar** — nylon, spans both side plates, retains lower axle. M3 clearance holes each end (1× per end).
- **Top crossbar** — nylon, spans both side plates. Carries 2× M6 heat set inserts positioned directly above the U-frame arms (not centred). M3 clearance holes each end (2× per end to resist uplift from adjustment force).

### U-Frame (upper assembly, single printed piece)
- Two arms that slide in the side plate cutouts
- Top crossbar connecting the arms — M6 bolt tips bear on this, directly above each arm
- Open-ended downward slots at the bottom of each arm to accept the upper axle (axle is retained by the side plate cutout walls once assembled)

### Rollers
- **2× rollers** — nylon, 25mm diameter × 40mm wide, smooth surface, 6mm axle bore

### Axles
- **2× 6mm steel rod** sections

### Crank
- Nylon, single piece L-shape (arm + handle)
- D-bore hub to match a flat filed on the lower axle rod
- Fitted to the lower axle

### Hardware
- 2× M6 threaded rod with brass thumbwheels (glued) — adjustment bolts
- 2× M6 heat set inserts (in top crossbar)
- M3 heat set inserts and M3 screws throughout for frame assembly

## Key Dimensions

| Item | Dimension |
|------|-----------|
| Roller diameter | 25mm |
| Roller width | 40mm |
| Axle diameter | 6mm |
| Side plate thickness | ~8mm |
| Side plate height | ~85mm |
| Overall device width | ~56mm (40mm roller + 2× 8mm side plates) |
| Adjustment travel (slot height) | ~15mm |
| Required adjustment range | ~1.5mm (1.3–2.5mm purfling) |
| M6 bolt positions | Directly above U-arms |

## Assembly Sequence

1. Drop lower roller and axle into side plate axle slots
2. Attach bottom crossbar with M3 screws — locks lower axle
3. Drop upper roller and axle into U-frame arm slots
4. Slide U-frame down into side plate cutouts — locks upper axle
5. Attach top crossbar with M3 screws (2× each end)
6. Install M6 heat set inserts in top crossbar
7. Thread M6 adjustment rods with thumbwheels through top crossbar
8. Attach crank to lower axle

## Notes

- Bolt tips should bear on flat pads on the U-frame crossbar directly above each arm to avoid point loading
- Plain bore nylon-on-steel bearing surfaces throughout — no bearings required at this load and speed
- Purfling enters by hand, operator ensures straight entry — no infeed guide needed
