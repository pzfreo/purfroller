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
arm_h    = 26.5       # U-frame arm height in Y — 5mm clearance above roller top
xbar_h   = 8.0        # U-frame top crossbar height
xbar_x_d = 25.0       # U-frame top crossbar depth in X (wide middle section only)
slot_w   = 6.1        # axle slot width in X (0.1mm clearance on 6mm axle)
slot_d   = 12.0       # axle slot depth in Y (open at arm bottom, U-shaped)
# Z-centre of each arm: sits mid-way through the side plate, just outside the roller
arm_z = roller_len / 2 + side_plate_t / 2   # = 24.0 mm
arm_z_inner = arm_z - arm_z_w / 2           # inner face of each arm in Z

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
# Axle slot cutter — U-shaped (rect + semicircular cap), open at Y=0
# Build at origin and subtract before moving arms to position; move() mutates in
# place so each arm must be constructed independently.
slot_r      = slot_w / 2
slot_rect   = Box(slot_w, slot_d - slot_r, arm_z_w + 2, align=(Align.CENTER, Align.MIN, Align.CENTER))
slot_cap    = Cylinder(radius=slot_r, height=arm_z_w + 2).move(Location((0, slot_d - slot_r, 0)))
slot_cutter = slot_rect + slot_cap

r_arm = (Box(arm_x_d, arm_h, arm_z_w, align=(Align.CENTER, Align.MIN, Align.CENTER)) - slot_cutter).move(Location((0, 0,  arm_z)))
l_arm = (Box(arm_x_d, arm_h, arm_z_w, align=(Align.CENTER, Align.MIN, Align.CENTER)) - slot_cutter).move(Location((0, 0, -arm_z)))

# Top crossbar — wide xbar_x_d boss in the Z-gap between the arms, narrowing to
# arm_x_d over each arm so the arms can slip-fit into a 14mm receiving slot.
xbar_mid = Box(
    xbar_x_d, xbar_h, 2 * arm_z_inner,
    align=(Align.CENTER, Align.MIN, Align.CENTER),
).move(Location((0, arm_h, 0)))
xbar_end_r = Box(arm_x_d, xbar_h, arm_z_w, align=(Align.CENTER, Align.MIN, Align.CENTER)).move(Location((0, arm_h,  arm_z)))
xbar_end_l = Box(arm_x_d, xbar_h, arm_z_w, align=(Align.CENTER, Align.MIN, Align.CENTER)).move(Location((0, arm_h, -arm_z)))
xbar = xbar_mid + xbar_end_r + xbar_end_l

u_frame = r_arm + l_arm + xbar
