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

arm_y_w  = 6.5        # U-frame arm width in Y (fits in 8mm side-plate slot with clearance)
arm_x_d  = 14.0       # U-frame arm depth in X (front-to-back) — 3.95mm wall each side of slot
arm_h    = 26.5       # U-frame arm height in Z — 5mm clearance between crossbar top and roller bottom
xbar_h   = 8.0        # U-frame crossbar height in Z (sits at the bottom of the inverted U)
xbar_x_d = 25.0       # U-frame crossbar depth in X (wider middle section between arms)
slot_w   = 6.1        # axle slot width in X (0.1mm clearance on 6mm axle)
slot_d   = 12.0       # axle slot depth in Z (open at arm top, U-shape with semicircular cap)
# Y-centre of each arm: sits mid-way through the side plate, just outside the roller
arm_y       = roller_len / 2 + side_plate_t / 2   # = 24.0 mm
arm_y_inner = arm_y - arm_y_w / 2                 # inner face of each arm in Y

# ── Roller ──────────────────────────────────────────────────────────────────
# Cylinder default axis is Z; rotate so axle lies along Y.
roller = (
    Cylinder(radius=roller_dia / 2, height=roller_len, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2, height=roller_len + 2, rotation=(90, 0, 0))
)

# ── U-Frame (inverted: crossbar at bottom, arms extending up) ───────────────
# Axle slot cutter — built in arm-local frame where Z=0 is the arm bottom (joins
# the crossbar) and Z=arm_h is the arm top (open end of the slot).
slot_r      = slot_w / 2
slot_rect   = Box(
    slot_w, arm_y_w + 2, slot_d - slot_r,
    align=(Align.CENTER, Align.CENTER, Align.MAX),
).move(Location((0, 0, arm_h)))
slot_cap    = Cylinder(
    radius=slot_r, height=arm_y_w + 2, rotation=(90, 0, 0),
).move(Location((0, 0, arm_h - (slot_d - slot_r))))
slot_cutter = slot_rect + slot_cap

# Arms — extend upward from the top of the crossbar (Z=xbar_h) to Z=xbar_h+arm_h.
r_arm = (Box(arm_x_d, arm_y_w, arm_h, align=(Align.CENTER, Align.CENTER, Align.MIN)) - slot_cutter).move(Location((0,  arm_y, xbar_h)))
l_arm = (Box(arm_x_d, arm_y_w, arm_h, align=(Align.CENTER, Align.CENTER, Align.MIN)) - slot_cutter).move(Location((0, -arm_y, xbar_h)))

# Crossbar at the bottom (Z=0 to Z=xbar_h) — wide xbar_x_d boss in the Y-gap
# between the arms (where the M6 adjustment bolts press up from below),
# narrowing to arm_x_d directly under each arm so the arms can slip-fit into
# the side plate slots.
xbar_mid    = Box(xbar_x_d, 2 * arm_y_inner, xbar_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
xbar_end_r  = Box(arm_x_d, arm_y_w, xbar_h, align=(Align.CENTER, Align.CENTER, Align.MIN)).move(Location((0,  arm_y, 0)))
xbar_end_l  = Box(arm_x_d, arm_y_w, xbar_h, align=(Align.CENTER, Align.CENTER, Align.MIN)).move(Location((0, -arm_y, 0)))
xbar        = xbar_mid + xbar_end_r + xbar_end_l

u_frame = r_arm + l_arm + xbar
