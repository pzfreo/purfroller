"""
Purfling Roller — build123d CAD model
Parts implemented: roller, axle, washer (×2), u_frame,
                   upper_roller, upper_axle, upper_washer (×2),
                   sp_r, sp_l (side plates), xbar_top (top crossbar),
                   xbar_bot (lower crossbar with M6 height-adjustment holes),
                   M3 heat-set inserts + bolts attaching crossbars to side plates
"""
from build123d import *

# ── Coordinate convention ───────────────────────────────────────────────────
# Z = vertical (up)
# Y = roller/axle axis (horizontal across)
# X = front-to-back (rolling direction)

# ── Parameters ─────────────────────────────────────────────────────────────
roller_dia   = 25.0   # roller OD (mm)
roller_len   = 56.0   # roller length (mm) — 56mm gives 60mm crossbar span (arm_y=34mm)
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
xbar_spine  = Box(arm_x_d, 2 * arm_y + arm_y_w, xbar_h, align=(Align.CENTER, Align.CENTER, Align.MIN))  # narrow spine spanning full Y, connects arms to mid boss
xbar_boss   = Box(xbar_x_d, 2 * (arm_y - side_plate_t / 2 - 0.5), xbar_h, align=(Align.CENTER, Align.CENTER, Align.MIN))  # wide boss in mid gap, 0.5mm clearance inside each side plate
xbar        = xbar_spine + xbar_boss

u_frame = r_arm + l_arm + xbar

# ── Outer frame parameters ───────────────────────────────────────────────────
upper_axle_z  = axle_z + 5.0 + roller_dia             # = 54.55 mm (gap=0 at max U-frame push)
frame_x_d     = 22.0   # side plate width in X (arm slot 14.2 + ~4mm wall each side)
frame_z_h     = 80.0   # top of frame in Z; plates run from xbar_h to frame_z_h
arm_slot_x    = arm_x_d + 0.2                         # = 14.2 mm slot with clearance
arm_slot_z    = 37.0   # slot height from plate base (xbar_h=8mm), reaches Z=45mm absolute
xbar_top_h    = 12.0   # top crossbar height; sits above upper roller (roller top ~67mm)
xbar_bot_h    = 15.0   # lower outer crossbar height; M6 height-adjustment bolts thread through it
xbar_top_y    = 2 * (arm_y - side_plate_t / 2)        # = 40.0 mm inner-face to inner-face
m6_dia        = 6.0    # M6 nominal thread diameter
# M6 heat-set insert (single central hole in xbar_bot, pressed in from below)
m6_hs_od      = 8.0    # insert OD
m6_hs_len     = 10.0   # insert length
m6_hs_dia     = 7.7    # hole dia (0.3mm under OD)
m6_clr_dia    = 6.2    # clearance hole above insert for bolt tip
m6_hs_chamfer = 0.4    # entry chamfer depth
plate_ext     = 30.0   # extra plate length below xbar_bot for bolt access
flange_y      = 40.0   # clamping flange outward width in Y (for G-clamps)
flange_z      = 10.0   # clamping flange thickness in Z

# ── Heat-set insert / M3 bolt parameters ─────────────────────────────────────
hs_insert_len = 5.0    # heat set insert length (mm) — 5mm OD brass M3 insert
hs_clear_len  = 8.0    # clearance behind insert for bolt tip
hs_dia        = 4.7    # hole dia (0.3mm under 5mm OD — grips on melt-in)
m3_clr_dia    = 3.3    # M3 clearance hole through side plate
hs_chamfer    = 0.4    # 45° entry chamfer depth to locate insert
bolt_x_off    = 6.0    # bolt X offset from centre (±); 2 bolts per crossbar end
hs_total      = hs_insert_len + hs_clear_len  # 13 mm total hole depth

def _hs_through_cutters(bolt_z_local, y_half):
    """2 through-bores for heat-set inserts (one per X offset), chamfered at both ends.
    Open at both ends so crossbars print upright with no supports."""
    cuts = []
    for bx in [+bolt_x_off, -bolt_x_off]:
        bore = Cylinder(
            radius=hs_dia / 2, height=2 * y_half + 2, rotation=(90, 0, 0)
        ).move(Location((bx, 0, bolt_z_local)))
        # +Y face chamfer: top_radius (at +Y) is wide, bottom_radius (at -Y) is narrow
        chf_p = Cone(
            bottom_radius=hs_dia / 2, top_radius=hs_dia / 2 + hs_chamfer,
            height=hs_chamfer, rotation=(90, 0, 0)
        ).move(Location((bx, y_half - hs_chamfer / 2, bolt_z_local)))
        # -Y face chamfer: bottom_radius (at -Y) is wide, top_radius (at +Y) is narrow
        chf_n = Cone(
            bottom_radius=hs_dia / 2 + hs_chamfer, top_radius=hs_dia / 2,
            height=hs_chamfer, rotation=(90, 0, 0)
        ).move(Location((bx, -y_half + hs_chamfer / 2, bolt_z_local)))
        cuts.append(bore + chf_p + chf_n)
    result = cuts[0]
    for c in cuts[1:]:
        result = result + c
    return result

def _m3_plate_cutters(bolt_zs_local):
    """M3 clearance holes through a side plate at given plate-local Z positions."""
    cuts = []
    for bx in [+bolt_x_off, -bolt_x_off]:
        for bz in bolt_zs_local:
            cuts.append(
                Cylinder(radius=m3_clr_dia / 2, height=side_plate_t + 2, rotation=(90, 0, 0))
                .move(Location((bx, 0, bz)))
            )
    result = cuts[0]
    for c in cuts[1:]:
        result = result + c
    return result

# ── Upper roller, axle and washers ───────────────────────────────────────────
upper_roller = (
    Cylinder(radius=roller_dia / 2, height=roller_len, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2, height=roller_len + 2, rotation=(90, 0, 0))
).move(Location((0, 0, upper_axle_z)))

upper_axle_stub = 15.0   # stub beyond each side plate for crank attachment (was 4mm)
upper_axle_len  = roller_len + 2 * washer_t + 2 * side_plate_t + 2 * upper_axle_stub  # = 86mm
upper_axle = Cylinder(radius=axle_dia / 2, height=upper_axle_len, rotation=(90, 0, 0)).move(Location((0, 0, upper_axle_z)))

upper_washer_r = (
    Cylinder(radius=washer_od / 2, height=washer_t, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2 + 0.2, height=washer_t + 2, rotation=(90, 0, 0))
).move(Location((0, +(roller_len / 2 + washer_t / 2), upper_axle_z)))
upper_washer_l = (
    Cylinder(radius=washer_od / 2, height=washer_t, rotation=(90, 0, 0))
    - Cylinder(radius=axle_dia / 2 + 0.2, height=washer_t + 2, rotation=(90, 0, 0))
).move(Location((0, -(roller_len / 2 + washer_t / 2), upper_axle_z)))

# ── Side plates ──────────────────────────────────────────────────────────────
# Plates run from Z=-(xbar_bot_h+plate_ext) to Z=frame_z_h.
# Extra 30mm below xbar_bot gives open access space for the M6 height-adjust bolt.
_plate_h       = frame_z_h + xbar_bot_h + plate_ext           # = 125.0 mm
_plate_z       = -(xbar_bot_h + plate_ext)                    # world Z of plate base = -45
_arm_slot_h    = arm_slot_z + xbar_h                         # = 45.0 mm (world Z=0 to 45)
_arm_slot_z    = xbar_bot_h + plate_ext                       # plate-local Z where slot starts = 45
_axle_hole_z   = upper_axle_z + xbar_bot_h + plate_ext        # = 99.55 mm plate-local
# M3 clearance holes at crossbar mid-heights (plate-local Z)
_sp_xbar_top_z = frame_z_h - xbar_top_h / 2 + xbar_bot_h + plate_ext   # = 119.0 mm plate-local
_sp_xbar_bot_z = xbar_bot_h / 2 + plate_ext                  # = 37.5 mm plate-local
_m3_cuts = _m3_plate_cutters([_sp_xbar_top_z, _sp_xbar_bot_z])
# G-clamp flanges in plate-local frame (Z=0 = plate base = world Z=-45).
# Each flange extends outward 40mm from the outer plate face at the bottom.
_flange_r = Box(frame_x_d, flange_y, flange_z,
                align=(Align.CENTER, Align.MIN, Align.MIN)
               ).move(Location((0, side_plate_t / 2, 0)))
_flange_l = Box(frame_x_d, flange_y, flange_z,
                align=(Align.CENTER, Align.MAX, Align.MIN)
               ).move(Location((0, -side_plate_t / 2, 0)))
sp_r = (
    Box(frame_x_d, side_plate_t, _plate_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    + _flange_r
    - Box(arm_slot_x, side_plate_t + 2, _arm_slot_h, align=(Align.CENTER, Align.CENTER, Align.MIN)).move(Location((0, 0, _arm_slot_z)))
    - Cylinder(radius=(axle_dia + 0.2) / 2, height=side_plate_t + 2, rotation=(90, 0, 0)).move(Location((0, 0, _axle_hole_z)))
    - _m3_cuts
).move(Location((0, +arm_y, _plate_z)))
sp_l = (
    Box(frame_x_d, side_plate_t, _plate_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    + _flange_l
    - Box(arm_slot_x, side_plate_t + 2, _arm_slot_h, align=(Align.CENTER, Align.CENTER, Align.MIN)).move(Location((0, 0, _arm_slot_z)))
    - Cylinder(radius=(axle_dia + 0.2) / 2, height=side_plate_t + 2, rotation=(90, 0, 0)).move(Location((0, 0, _axle_hole_z)))
    - _m3_cuts
).move(Location((0, -arm_y, _plate_z)))

# ── Top crossbar ─────────────────────────────────────────────────────────────
# Structural tie between side plates above the upper roller (roller top ~67mm).
# Upper axle retained by side plate holes. 2 M3 bolts per end into heat-set inserts.
xbar_top = (
    Box(frame_x_d, xbar_top_y, xbar_top_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    - _hs_through_cutters(xbar_top_h / 2, xbar_top_y / 2)
).move(Location((0, 0, frame_z_h - xbar_top_h)))

# ── Lower crossbar ───────────────────────────────────────────────────────────
# Sits below the U-frame crossbar (Z=-xbar_bot_h to Z=0).
# Two M6 heat-set inserts at Y=±xbar_top_y/6 (third-points of the inner span)
# so the adjustment bolts give lateral stability to the U-frame.
# 2 M3 bolts per end into heat-set inserts attach to side plates.
m6_y_off = 15.0   # ±15mm from centre; 15mm gap to each side plate inner face (±30mm)

def _make_m6_cutter(y_off):
    """Single M6 heat-set cutter at the given Y offset (new object each call — avoids move() aliasing)."""
    return (
        Cone(bottom_radius=m6_hs_dia / 2 + m6_hs_chamfer, top_radius=m6_hs_dia / 2,
             height=m6_hs_chamfer, align=(Align.CENTER, Align.CENTER, Align.MIN))
        + Cylinder(radius=m6_hs_dia / 2, height=m6_hs_len + 1,
                   align=(Align.CENTER, Align.CENTER, Align.MIN))
        + Cylinder(radius=m6_clr_dia / 2, height=(xbar_bot_h - m6_hs_len) + 2,
                   align=(Align.CENTER, Align.CENTER, Align.MIN)).move(Location((0, 0, m6_hs_len)))
    ).move(Location((0, y_off, 0)))

xbar_bot = (
    Box(frame_x_d, xbar_top_y, xbar_bot_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    - _make_m6_cutter(+m6_y_off)
    - _make_m6_cutter(-m6_y_off)
    - _hs_through_cutters(xbar_bot_h / 2, xbar_top_y / 2)
).move(Location((0, 0, -xbar_bot_h)))

# ── Crank parameters ─────────────────────────────────────────────────────────
hub_od          = 16.0   # crank hub OD
hub_len         = 15.0   # hub length along Y (sits on axle stub outside right plate)
crank_arm_len   = 40.0   # axle centre to handle bore centre (mm)
crank_arm_h     = 10.0   # arm height in Z
post_od         = 10.0   # handle post OD
post_len        = hub_len + 0.5  # 0.5mm protrusion past inner crank face gives running clearance for rotation
post_bore_dia   = 10.4   # arm bore for post (0.4mm clearance)
post_flange_od  = 14.0
post_flange_h   = 2.0
handle_od       = 16.0
handle_len      = 30.0
ret_washer_od   = 14.0
ret_washer_h    = 4.0

# Key Y positions — crank on right (+Y) side
hub_y_inner = arm_y + side_plate_t / 2           # = 28mm (plate outer face)
hub_y_c     = hub_y_inner + hub_len / 2          # = 35.5mm (hub centre)
arm_y_outer = hub_y_inner + hub_len              # = 43mm (arm outer face)
post_tip_y        = arm_y_outer - post_len             # = 34.7mm (inner end of post)
handle_body_y_c   = arm_y_outer + post_flange_h + handle_len / 2  # = 60mm

# ── Crank (hub + arm, one printed piece) ─────────────────────────────────────
# Two circular bosses (hub and handle end) joined by rectangular arm.
# Hub clamped to axle by M3 bolt into radial heat-set insert on hub top.
_hub_boss    = Cylinder(radius=hub_od / 2, height=hub_len,
                        rotation=(90, 0, 0)).move(Location((0, hub_y_c, upper_axle_z)))
_handle_boss = Cylinder(radius=hub_od / 2, height=hub_len,
                        rotation=(90, 0, 0)).move(Location((crank_arm_len, hub_y_c, upper_axle_z)))
_arm_box     = Box(crank_arm_len, hub_len, crank_arm_h,
                   align=(Align.MIN, Align.CENTER, Align.CENTER)
                  ).move(Location((0, hub_y_c, upper_axle_z)))
_axle_bore   = Cylinder(radius=axle_dia / 2, height=hub_len + 2,
                        rotation=(90, 0, 0)).move(Location((0, hub_y_c, upper_axle_z)))
_hub_top_z   = upper_axle_z + hub_od / 2
_hub_insert  = (
    Cone(bottom_radius=hs_dia / 2, top_radius=hs_dia / 2 + hs_chamfer,
         height=hs_chamfer, align=(Align.CENTER, Align.CENTER, Align.MAX))
    + Cylinder(radius=hs_dia / 2, height=hs_insert_len + 1,
               align=(Align.CENTER, Align.CENTER, Align.MAX))
    + Cylinder(radius=m3_clr_dia / 2,
               height=(hub_od / 2 - axle_dia / 2 - hs_insert_len) + 2,
               align=(Align.CENTER, Align.CENTER, Align.MAX)
              ).move(Location((0, 0, -hs_insert_len)))
).move(Location((0, hub_y_c, _hub_top_z)))
_post_bore   = Cylinder(radius=post_bore_dia / 2, height=hub_len + 2,
                        rotation=(90, 0, 0)).move(Location((crank_arm_len, hub_y_c, upper_axle_z)))
crank = _hub_boss + _handle_boss + _arm_box - _axle_bore - _hub_insert - _post_bore

# ── Handle (separate spinning piece, same pattern as peg-turner) ─────────────
# post → inside arm bore (Y=post_tip_y to arm_y_outer)
# flange → sits on arm outer face (Y=arm_y_outer to arm_y_outer+post_flange_h)
# body → outward grip beyond flange
_handle_post = Cylinder(radius=post_od / 2, height=post_len,
                        rotation=(90, 0, 0)
                       ).move(Location((crank_arm_len, post_tip_y + post_len / 2, upper_axle_z)))
_handle_flng = Cylinder(radius=post_flange_od / 2, height=post_flange_h,
                        rotation=(90, 0, 0)
                       ).move(Location((crank_arm_len, arm_y_outer + post_flange_h / 2, upper_axle_z)))
_handle_body = Cylinder(radius=handle_od / 2, height=handle_len,
                        rotation=(90, 0, 0)
                       ).move(Location((crank_arm_len, handle_body_y_c, upper_axle_z)))
_post_insert = Cylinder(radius=hs_dia / 2, height=hs_insert_len + 1,
                        rotation=(90, 0, 0)
                       ).move(Location((crank_arm_len, post_tip_y + (hs_insert_len + 1) / 2, upper_axle_z)))
handle = _handle_body + _handle_post + _handle_flng - _post_insert

# ── Retaining washer ─────────────────────────────────────────────────────────
# Sits against arm inner face (Y=hub_y_inner=28mm), held by M3 bolt into post insert.
ret_washer = (
    Cylinder(radius=ret_washer_od / 2, height=ret_washer_h, rotation=(90, 0, 0))
    - Cylinder(radius=m3_clr_dia / 2, height=ret_washer_h + 2, rotation=(90, 0, 0))
).move(Location((crank_arm_len, post_tip_y - ret_washer_h / 2, upper_axle_z)))
