"""Thumb wheel — M6 flat-head bolt, printed ISO thread, vertical grip flutes."""
from math import cos, sin, radians
from build123d import *
from bd_warehouse.thread import IsoThread

# ── Parameters ──────────────────────────────────────────────────────────────
od        = 25.0   # outer diameter (mm)
height    = 10.0   # wheel height (mm)
n_flutes  = 9      # grip flutes around circumference
flute_r   = 2.0    # flute cutter radius (mm) — semi-circle bite into edge
cs_od     = 12.0   # countersink OD at top face (mm) — M6 flat head bearing surface
cs_depth  = 4.0    # countersink depth (mm)
m6_dia    = 6.0    # M6 major diameter (mm)
m6_pitch  = 1.0    # M6 coarse pitch (mm)
# M6x1 minor radius (ISO 68-1): bolt shaft fits through this bore when threading
m6_bore_r   = 2.5    # 5.0mm bore — standard M6 tap drill, generous for printed plastic
m6_lead_depth = 1.5  # lead-in chamfer depth at bottom entry (mm)

# ── Main body ────────────────────────────────────────────────────────────────
body = Cylinder(radius=od / 2, height=height, align=(Align.CENTER, Align.CENTER, Align.MIN))

# ── Grip flutes — 9 vertical semi-circular grooves around the edge ───────────
flute_cutters = []
for i in range(n_flutes):
    angle = radians(i * 360.0 / n_flutes)
    cx = (od / 2) * cos(angle)
    cy = (od / 2) * sin(angle)
    flute_cutters.append(
        Cylinder(radius=flute_r, height=height + 2,
                 align=(Align.CENTER, Align.CENTER, Align.MIN))
        .move(Location((cx, cy, -1)))
    )
flute_solid = flute_cutters[0]
for f in flute_cutters[1:]:
    flute_solid = flute_solid + f

# ── Countersink for M6 flat head (wide at top face, narrows to thread bore) ──
# Cone: bottom (narrow, at Z=height-cs_depth) → top (wide, at Z=height)
countersink = Cone(
    bottom_radius=m6_dia / 2,
    top_radius=cs_od / 2,
    height=cs_depth,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
).move(Location((0, 0, height - cs_depth)))

# ── Through-bore: IsoThread end caps block the hole without this ─────────────
bore = Cylinder(radius=m6_bore_r, height=height + 2,
                align=(Align.CENTER, Align.CENTER, Align.MIN)).move(Location((0, 0, -1)))

# ── Lead-in chamfer at bottom entry: 6mm → 5mm over 1.5mm depth ──────────────
lead_in = Cone(bottom_radius=m6_dia / 2, top_radius=m6_bore_r, height=m6_lead_depth,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

# ── M6 printed internal thread (full depth; countersink clears the top) ──────
thread = IsoThread(
    major_diameter=m6_dia,
    pitch=m6_pitch,
    length=height,
    external=False,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

# ── Boolean assembly ─────────────────────────────────────────────────────────
thumb_wheel = body - flute_solid - countersink - bore - lead_in - thread

# ── Fillets — outer rim and flute-bottom edges at top and bottom faces ────────
def _edge_r(e):
    c = e.center()
    return (c.X**2 + c.Y**2)**0.5

_top_bot = (thumb_wheel.edges().filter_by_position(Axis.Z, -0.1, 0.1) +
            thumb_wheel.edges().filter_by_position(Axis.Z, height - 0.1, height + 0.1))
thumb_wheel = fillet([e for e in _top_bot if _edge_r(e) > 11.0], radius=1.5)

_top_bot2 = (thumb_wheel.edges().filter_by_position(Axis.Z, -0.1, 0.1) +
             thumb_wheel.edges().filter_by_position(Axis.Z, height - 0.1, height + 0.1))
thumb_wheel = fillet([e for e in _top_bot2 if 7.0 < _edge_r(e) < 11.0], radius=0.6)
