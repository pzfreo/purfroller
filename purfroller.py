"""
Purfling Roller — build123d CAD model
Parts implemented: roller, u_frame
See SPEC.md for full design details.
"""
from build123d import *

# ── Parameters ─────────────────────────────────────────────────────────────
roller_dia   = 25.0   # roller OD (mm)
roller_len   = 40.0   # roller length (mm)
axle_dia     = 6.0    # steel axle rod diameter (mm)
side_plate_t = 8.0    # side plate thickness in Z (along axle)

arm_z_w  = 6.5        # U-frame arm width in Z (fits in 8mm side-plate cutout with clearance)
arm_x_d  = 14.0       # U-frame arm depth in X (front-to-back) — 3.95mm wall each side of slot
arm_h    = 50.0       # U-frame arm height in Y
xbar_h   = 8.0        # U-frame top crossbar height
xbar_x_d = 10.0       # U-frame top crossbar depth in X
slot_w   = 6.1        # axle slot width in X (0.1mm clearance on 6mm axle)
slot_d   = 12.0       # axle slot depth in Y (open at arm bottom, U-shaped)
pad_sz   = 8.0        # M6 bearing-pad footprint (mm)
pad_h    = 2.0        # M6 bearing-pad height (mm)

# Z-centre of each arm: sits mid-way through the side plate, just outside the roller
arm_z = roller_len / 2 + side_plate_t / 2   # = 24.0 mm

# ── Coordinate convention ───────────────────────────────────────────────────
# Z = roller/axle axis
# Y = vertical (up)
# X = front-to-back

# ── Roller ──────────────────────────────────────────────────────────────────
roller = (
    Cylinder(radius=roller_dia / 2, height=roller_len)
    - Cylinder(radius=axle_dia / 2, height=roller_len + 2)
)

# ── U-Frame ─────────────────────────────────────────────────────────────────
# Arms — bottom face at Y=0, centred in X, positioned at ±arm_z in Z
r_arm = Box(
    arm_x_d, arm_h, arm_z_w,
    align=(Align.CENTER, Align.MIN, Align.CENTER),
).move(Location((0, 0,  arm_z)))

l_arm = Box(
    arm_x_d, arm_h, arm_z_w,
    align=(Align.CENTER, Align.MIN, Align.CENTER),
).move(Location((0, 0, -arm_z)))

# Top crossbar — bottom flush with top of arms, spans full arm-to-arm width in Z
xbar = Box(
    xbar_x_d, xbar_h, 2 * arm_z + arm_z_w,
    align=(Align.CENTER, Align.MIN, Align.CENTER),
).move(Location((0, arm_h, 0)))

# M6 bearing pads on top of crossbar, centred above each arm
r_pad = Box(
    pad_sz, pad_h, pad_sz,
    align=(Align.CENTER, Align.MIN, Align.CENTER),
).move(Location((0, arm_h + xbar_h,  arm_z)))

l_pad = Box(
    pad_sz, pad_h, pad_sz,
    align=(Align.CENTER, Align.MIN, Align.CENTER),
).move(Location((0, arm_h + xbar_h, -arm_z)))

# Axle slots — U-shaped (rectangular lower portion + semicircular cap), open at Y=0
slot_r = slot_w / 2
slot_rect = Box(slot_w, slot_d - slot_r, arm_z_w + 2, align=(Align.CENTER, Align.MIN, Align.CENTER))
slot_cap  = Cylinder(radius=slot_r, height=arm_z_w + 2).move(Location((0, slot_d - slot_r, 0)))
slot_cutter = slot_rect + slot_cap

r_slot = slot_cutter.move(Location((0, 0,  arm_z)))
l_slot = slot_cutter.move(Location((0, 0, -arm_z)))

u_frame = (r_arm + l_arm + xbar + r_pad + l_pad) - r_slot - l_slot
