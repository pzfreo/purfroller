"""
Purfling Roller — build123d CAD model
Parts implemented: roller, u_frame
See SPEC.md for full design details.
"""
from build123d import *

# ── Coordinate convention ───────────────────────────────────────────────────
# Z = vertical (up)
# Y = roller/axle axis (horizontal across)
# X = front-to-back (rolling direction)

# ── Parameters ─────────────────────────────────────────────────────────────
roller_dia   = 25.0   # roller OD (mm)
roller_len   = 40.0   # roller length (mm)
axle_dia     = 6.0    # steel axle rod diameter (mm)
side_plate_t = 8.0    # side plate thickness in Y (along axle)

arm_y_w  = 6.5        # U-frame arm width in Y (fits in 8mm side-plate cutout with clearance)
arm_x_d  = 14.0       # U-frame arm depth in X (front-to-back) — 3.95mm wall each side of slot
arm_h    = 26.5       # U-frame arm height in Z — 5mm clearance above roller top
xbar_h   = 8.0        # U-frame top crossbar height in Z
xbar_x_d = 25.0       # U-frame top crossbar depth in X (wide middle section only)
slot_w   = 6.1        # axle slot width in X (0.1mm clearance on 6mm axle)
slot_d   = 12.0       # axle slot depth in Z (open at arm bottom, U-shaped)
# Y-centre of each arm: sits mid-way through the side plate, just outside the roller
arm_y = roller_len / 2 + side_plate_t / 2   # = 24.0 mm
arm_y_inner = arm_y - arm_y_w / 2           # inner face of each arm in Y

# ── Roller ──────────────────────────────────────────────────────────────────
# Cylinder default axis is Z; rotate so axle lies along Y.
roller = (
    Cylinder(radius=roller_dia / 2, height=roller_len, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2, height=roller_len + 2, rotation=(90, 0, 0))
)

# ── U-Frame ─────────────────────────────────────────────────────────────────
# Axle slot cutter — U-shaped (rect + semicircular cap), open at Z=0.
# Built at origin and subtracted before moving arms to position.
slot_r      = slot_w / 2
slot_rect   = Box(slot_w, arm_y_w + 2, slot_d - slot_r, align=(Align.CENTER, Align.CENTER, Align.MIN))
slot_cap    = Cylinder(radius=slot_r, height=arm_y_w + 2, rotation=(90, 0, 0)).move(Location((0, 0, slot_d - slot_r)))
slot_cutter = slot_rect + slot_cap

r_arm = (Box(arm_x_d, arm_y_w, arm_h, align=(Align.CENTER, Align.CENTER, Align.MIN)) - slot_cutter).move(Location((0,  arm_y, 0)))
l_arm = (Box(arm_x_d, arm_y_w, arm_h, align=(Align.CENTER, Align.CENTER, Align.MIN)) - slot_cutter).move(Location((0, -arm_y, 0)))

# Top crossbar — wide xbar_x_d boss in the Y-gap between the arms, narrowing to
# arm_x_d over each arm so the arms can slip-fit into a 14mm receiving slot.
xbar_mid = Box(
    xbar_x_d, 2 * arm_y_inner, xbar_h,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).move(Location((0, 0, arm_h)))
xbar_end_r = Box(arm_x_d, arm_y_w, xbar_h, align=(Align.CENTER, Align.CENTER, Align.MIN)).move(Location((0,  arm_y, arm_h)))
xbar_end_l = Box(arm_x_d, arm_y_w, xbar_h, align=(Align.CENTER, Align.CENTER, Align.MIN)).move(Location((0, -arm_y, arm_h)))
xbar = xbar_mid + xbar_end_r + xbar_end_l

u_frame = r_arm + l_arm + xbar
