# Rectangular backing plate

A solid, flat rectangular plate measuring **399.5 × 299.5 × 3.5 mm** (X × Y × Z), with square corners and no holes, recesses, or other features. The lower corner is at `(0, 0, 0)` and the bottom surface lies on Z = 0.

Both broad faces are flat and uninterrupted: **no grooves, ribs, embossing, or texture**. The STL triangles lie in the same planes and do not form physical seams or grooves. A smooth finish is the intended result; actual printed surface quality depends on the printing process and any finishing work. If finishing removes material, account for it when checking the final 3.5 mm thickness.

## Files

- `models/backing_plate.scad`: editable, parameterized OpenSCAD model.
- `backing_plate_399p5x299p5x3p5mm.stl`: ready to import into a slicer; dimensions are in millimeters.
- `scripts/generate_plate.py`: generate the STL using Python's standard library.
- `scripts/verify_plate.py`: check dimensions, triangle area, outward winding, closed edges, and volume; exits with a failure code if a check fails.

## Generate and verify

Run from the repository root with Python 3:

```sh
python scripts/generate_plate.py
python scripts/verify_plate.py
```

To generate another size, set each dimension independently so changing length or width does not unintentionally change thickness:

```sh
python scripts/generate_plate.py --length 399.5 --width 299.5 --thickness 3.5 --output files/custom_plate.stl
python scripts/verify_plate.py files/custom_plate.stl --length 399.5 --width 299.5 --thickness 3.5
```

Alternatively, edit the dimensions in `models/backing_plate.scad` and export STL from OpenSCAD. STL itself does not encode units; import using millimeters and 100% scale.

## Printing

Place the 399.5 × 299.5 mm face flat on the build plate. The geometry has no overhangs and needs no supports in that orientation. Check usable printer build area before slicing: the part needs a 399.5 × 299.5 mm footprint, with additional space if a brim is used. Choose material and slicer settings for the intended use. This model has not yet been physically printed or fit tested.

## Project origin

This repository follows the model-file plus Python-utility approach of [pool-skimmer-3dprint](https://github.com/sofia-vinas/pool-skimmer-3dprint), but its geometry is generated from the dimensions above. No pool-skimmer mesh or third-party model assets are included. There is no inherited Thingiverse attribution or license for this new geometry; a project license has not yet been selected.
