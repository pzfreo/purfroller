"""
Purfling Roller — build123d CAD model
Parts implemented: roller, axle, washer (×2), u_frame,
                   upper_roller, upper_axle, upper_washer (×2),
                   sp_r, sp_l (side plates), xbar_top (top crossbar)
"""
from build123d import *

# ── Coordinate convention ───────────────────────────────────────────────────
# Z = vertical (up)
# Y = roller/axle axis (horizontal across)
# X = front-to-back (rolling direction)

# ── Parameters ─────────────────────────────────────────────────────────────
roller_dia   = 25.0   # roller OD (mm)
roller_len   = 36.0   # roller length (mm) — shortened 4 mm to give washer clearance
axle_dia     = 4.0    # steel axle rod diameter (mm)
side_plate_t = 8.0    # side plate thickness in Y (arm slides through this)
washer_t     = 2.0    # thrust washer thickness in Y (between roller end and side plate)
washer_od    = 12.0   # thrust washer outer diameter

arm_y_w  = 6.5        # U-frame arm width in Y (arm slides through side_plate_t slot, 0.75 mm clearance each side)
arm_x_d  = 14.0       # U-frame arm depth in X (front-to-back) — 4.95mm wall each side of slot
arm_h    = 26.5       # U-frame arm height in Z — ~4mm clearance between crossbar top and roller bottom
xbar_h   = 8.0        # U-frame crossbar height in Z (sits at the bottom of the inverted U)
xbar_x_d = 25.0       # U-frame crossbar depth in X (wider middle section between arms)
slot_w   = 4.1        # axle slot width in X (0.1mm clearance on 4mm axle)
slot_d   = 12.0       # axle slot depth in Z (open at arm top, U-shape with semicircular cap)
# Y-centre of each arm: washer fills gap between roller end and side plate inner face
arm_y       = roller_len / 2 + washer_t + side_plate_t / 2   # = 18+2+4 = 24.0 mm
arm_y_inner = arm_y - arm_y_w / 2                            # inner face of each arm in Y
# Axle centre height in global Z — derived from slot geometry
axle_z      = xbar_h + arm_h - (slot_d - slot_w / 2)         # = 24.55 mm
# Axle total length: roller + 2 washers + 2 side plates + 4 mm stub each side
axle_len    = roller_len + 2 * washer_t + 2 * side_plate_t + 8  # = 64.0 mm

# ── Roller ──────────────────────────────────────────────────────────────────
# Cylinder default axis is Z; rotate so axle lies along Y.
roller = (
    Cylinder(radius=roller_dia / 2, height=roller_len, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2, height=roller_len + 2, rotation=(90, 0, 0))
).move(Location((0, 0, axle_z)))

# ── Axle ────────────────────────────────────────────────────────────────────
axle = Cylinder(radius=axle_dia / 2, height=axle_len, rotation=(90, 0, 0)).move(Location((0, 0, axle_z)))

# ── Washers (thrust spacers between roller ends and side plate inner faces) ──
washer_r = (
    Cylinder(radius=washer_od / 2, height=washer_t, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2 + 0.2, height=washer_t + 2, rotation=(90, 0, 0))
).move(Location((0, +(roller_len / 2 + washer_t / 2), axle_z)))
washer_l = (
    Cylinder(radius=washer_od / 2, height=washer_t, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2 + 0.2, height=washer_t + 2, rotation=(90, 0, 0))
).move(Location((0, -(roller_len / 2 + washer_t / 2), axle_z)))

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

# ── Outer frame parameters ───────────────────────────────────────────────────
upper_axle_z  = axle_z + 5.0 + roller_dia             # = 54.55 mm (gap=0 at max U-frame push)
frame_x_d     = 22.0   # side plate width in X (arm slot 14.2 + ~4mm wall each side)
frame_z_h     = 80.0   # top of frame in Z; plates run from xbar_h to frame_z_h
arm_slot_x    = arm_x_d + 0.2                         # = 14.2 mm slot with clearance
arm_slot_z    = 37.0   # slot height from plate base (xbar_h=8mm), reaches Z=45mm absolute
xbar_top_h    = 12.0   # top crossbar height; sits above upper roller (roller top ~67mm)
xbar_top_y    = 2 * (arm_y - side_plate_t / 2)        # = 40.0 mm inner-face to inner-face

# ── Upper roller, axle and washers ───────────────────────────────────────────
upper_roller = (
    Cylinder(radius=roller_dia / 2, height=roller_len, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2, height=roller_len + 2, rotation=(90, 0, 0))
).move(Location((0, 0, upper_axle_z)))

upper_axle = Cylinder(radius=axle_dia / 2, height=axle_len, rotation=(90, 0, 0)).move(Location((0, 0, upper_axle_z)))

upper_washer_r = (
    Cylinder(radius=washer_od / 2, height=washer_t, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2 + 0.2, height=washer_t + 2, rotation=(90, 0, 0))
).move(Location((0, +(roller_len / 2 + washer_t / 2), upper_axle_z)))
upper_washer_l = (
    Cylinder(radius=washer_od / 2, height=washer_t, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2 + 0.2, height=washer_t + 2, rotation=(90, 0, 0))
).move(Location((0, -(roller_len / 2 + washer_t / 2), upper_axle_z)))

# ── Side plates ──────────────────────────────────────────────────────────────
# Plates start at Z=xbar_h so the U-frame crossbar hangs below without clashing.
# Arm guide slot open at plate base. Upper axle hole in plate-local Z coords.
# M3 bolt holes added later.
_plate_h   = frame_z_h - xbar_h                               # = 72.0 mm
_axle_hole_z = upper_axle_z - xbar_h                          # = 46.55 mm in plate-local Z
sp_r = (
    Box(frame_x_d, side_plate_t, _plate_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    - Box(arm_slot_x, side_plate_t + 2, arm_slot_z, align=(Align.CENTER, Align.CENTER, Align.MIN))
    - Cylinder(radius=(axle_dia + 0.2) / 2, height=side_plate_t + 2, rotation=(90, 0, 0)).move(Location((0, 0, _axle_hole_z)))
).move(Location((0, +arm_y, xbar_h)))
sp_l = (
    Box(frame_x_d, side_plate_t, _plate_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    - Box(arm_slot_x, side_plate_t + 2, arm_slot_z, align=(Align.CENTER, Align.CENTER, Align.MIN))
    - Cylinder(radius=(axle_dia + 0.2) / 2, height=side_plate_t + 2, rotation=(90, 0, 0)).move(Location((0, 0, _axle_hole_z)))
).move(Location((0, -arm_y, xbar_h)))

# ── Top crossbar ─────────────────────────────────────────────────────────────
# Structural tie between side plates above the upper roller (roller top ~67mm).
# Upper axle is held by side plate holes alone. M3 inserts added later.
xbar_top = Box(frame_x_d, xbar_top_y, xbar_top_h, align=(Align.CENTER, Align.CENTER, Align.MIN)).move(Location((0, 0, frame_z_h - xbar_top_h)))
