"""Export all printed parts from purfroller.py as STEP files for estampo."""
import os
import runpy
from build123d import export_step

os.makedirs("parts", exist_ok=True)

ns = runpy.run_path("purfroller.py")

parts = [
    "roller",
    "u_frame",
    "upper_roller",
    "sp_r",
    "sp_l",
    "xbar_top",
    "xbar_bot",
    "washer_r",
    "washer_l",
    "upper_washer_r",
    "upper_washer_l",
    "crank",
    "handle",
    "ret_washer",
]

for name in parts:
    path = f"parts/{name}.step"
    export_step(ns[name], path)
    print(f"exported {path}")

# Assembly: all parts combined into a single STEP file
from build123d import Compound
assembly = Compound(children=[ns[name] for name in parts])
export_step(assembly, "parts/assembly.step")
print("exported parts/assembly.step")
