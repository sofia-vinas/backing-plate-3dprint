"""Generate an outward-wound ASCII STL rectangular plate; no dependencies."""
import argparse
import math
from pathlib import Path

DEFAULT_OUTPUT = Path(__file__).resolve().parent / "backing_plate_399p5x299p5x3p5mm.stl"


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("Dimension must be finite and positive")
    return number


def plate_triangles(length, width, thickness):
    vertices = [(0, 0, 0), (length, 0, 0), (length, width, 0), (0, width, 0),
                (0, 0, thickness), (length, 0, thickness),
                (length, width, thickness), (0, width, thickness)]
    faces = [((0, 0, -1), (0, 3, 2, 1)), ((0, 0, 1), (4, 5, 6, 7)),
             ((0, -1, 0), (0, 1, 5, 4)), ((1, 0, 0), (1, 2, 6, 5)),
             ((0, 1, 0), (2, 3, 7, 6)), ((-1, 0, 0), (3, 0, 4, 7))]
    for normal, (a, b, c, d) in faces:
        for indices in [(a, b, c), (a, c, d)]:
            yield normal, tuple(vertices[i] for i in indices)


def write_plate(path, length, width, thickness):
    if any(not math.isfinite(v) or v <= 0 for v in (length, width, thickness)):
        raise ValueError("Dimensions must be finite and positive")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["solid backing_plate"]
    for normal, triangle in plate_triangles(length, width, thickness):
        lines.append("  facet normal " + " ".join(format(n, ".17g") for n in normal))
        lines.append("    outer loop")
        for vertex in triangle:
            lines.append("      vertex " + " ".join(format(v, ".17g") for v in vertex))
        lines.extend(["    endloop", "  endfacet"])
    lines.append("endsolid backing_plate")
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length", type=positive, default=399.5)
    parser.add_argument("--width", type=positive, default=299.5)
    parser.add_argument("--thickness", type=positive, default=3.5)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    write_plate(args.output, args.length, args.width, args.thickness)
    print(f"Wrote {args.output}: {args.length:g} × {args.width:g} × {args.thickness:g} mm (12 triangles)")


if __name__ == "__main__":
    main()
