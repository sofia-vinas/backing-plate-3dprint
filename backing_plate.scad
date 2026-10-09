// Rectangular backing plate. All dimensions in millimeters.
// Flat, uninterrupted faces: no grooves, ribs, embossing, or texture.
length_mm = 400;
width_mm = 300;
thickness_mm = 3.5;

assert(length_mm > 0 && width_mm > 0 && thickness_mm > 0,
       "All dimensions must be positive.");
cube([length_mm, width_mm, thickness_mm], center = false);
