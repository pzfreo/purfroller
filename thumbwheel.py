"""Thumb wheel — M6 flat-head bolt, printed ISO thread, vertical grip flutes."""
from math import cos, sin, radians
from build123d import *
from bd_warehouse.thread import IsoThread

# ── Parameters ──────────────────────────────────────────────────────────────
od        = 25.0   # outer diameter (mm)
height    = 10.0   # wheel height (mm)
n_flutes  = 9      # grip flutes around circumference
flute_r   = 3.5    # flute cutter radius (mm) — semi-circle bite into edge
cs_od     = 12.0   # countersink OD at top face (mm) — M6 flat head bearing surface
cs_depth  = 4.0    # countersink depth (mm)
m6_dia    = 6.0    # M6 major diameter (mm)
m6_pitch  = 1.0    # M6 coarse pitch (mm)

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

# ── M6 printed internal thread (full depth; countersink clears the top) ──────
thread = IsoThread(
    major_diameter=m6_dia,
    pitch=m6_pitch,
    length=height,
    external=False,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

# ── Final shape ──────────────────────────────────────────────────────────────
thumb_wheel = body - flute_solid - countersink - thread
