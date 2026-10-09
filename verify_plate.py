"""Verify a rectangular plate STL's dimensions and mesh; no dependencies."""
import argparse
from collections import Counter
import math
from pathlib import Path
import struct
import sys

from generate_plate import DEFAULT_OUTPUT, positive


def read_triangles(path):
    data = Path(path).read_bytes()
    if len(data) >= 84:
        count = struct.unpack_from("<I", data, 80)[0]
        if len(data) == 84 + count * 50:
            triangles = []
            for index in range(count):
                values = struct.unpack_from("<12fH", data, 84 + index * 50)
                triangles.append(tuple(tuple(values[i:i + 3]) for i in (3, 6, 9)))
            return triangles
    lines = [line.strip().split() for line in data.decode("ascii").splitlines() if line.strip()]
    if not lines or lines[0][0] != "solid" or lines[-1][0] != "endsolid":
        raise ValueError("Invalid or truncated STL")
    triangles = []
    index = 1
    while index < len(lines) - 1:
        block = lines[index:index + 7]
        if (len(block) != 7 or block[0][:2] != ["facet", "normal"]
                or len(block[0]) != 5 or block[1] != ["outer", "loop"]
                or block[5] != ["endloop"] or block[6] != ["endfacet"]
                or any(len(row) != 4 or row[0] != "vertex" for row in block[2:5])):
            raise ValueError("Invalid or truncated ASCII STL facet")
        triangles.append(tuple(tuple(float(v) for v in row[1:]) for row in block[2:5]))
        index += 7
    if index != len(lines) - 1:
        raise ValueError("Invalid STL ending")
    return triangles


def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def verify(path, expected, tolerance=0.001):
    triangles = read_triangles(path)
    if not triangles:
        raise ValueError("Mesh has no triangles")
    vertices = [v for triangle in triangles for v in triangle]
    if any(not math.isfinite(value) for v in vertices for value in v):
        raise ValueError("Mesh contains non-finite coordinates")
    minimum = tuple(min(v[i] for v in vertices) for i in range(3))
    maximum = tuple(max(v[i] for v in vertices) for i in range(3))
    size = tuple(hi - lo for lo, hi in zip(minimum, maximum))
    if any(abs(actual - target) > tolerance for actual, target in zip(size, expected)):
        raise ValueError(f"Dimensions {size} do not match {expected} mm")
    if any(abs(v) > tolerance for v in minimum):
        raise ValueError(f"Expected minimum corner at origin, got {minimum}")
    center = tuple((lo + hi) / 2 for lo, hi in zip(minimum, maximum))
    edges = Counter()
    volume = 0.0
    for a, b, c in triangles:
        normal = cross(tuple(b[i] - a[i] for i in range(3)), tuple(c[i] - a[i] for i in range(3)))
        if dot(normal, normal) == 0:
            raise ValueError("Degenerate triangle")
        centroid = tuple((a[i] + b[i] + c[i]) / 3 - center[i] for i in range(3))
        if dot(normal, centroid) <= 0:
            raise ValueError("Triangle winding is not outward for a convex plate")
        for edge in ((a, b), (b, c), (c, a)):
            edges[edge] += 1
        volume += dot(a, cross(b, c)) / 6
    for (a, b), count in edges.items():
        if count != 1 or edges[(b, a)] != 1:
            raise ValueError("Mesh has an open, duplicate, or non-manifold edge")
    target_volume = math.prod(expected)
    if not math.isclose(volume, target_volume, rel_tol=1e-6, abs_tol=tolerance):
        raise ValueError(f"Volume {volume:g} does not match {target_volume:g} mm³")
    print(f"PASS: {size[0]:g} × {size[1]:g} × {size[2]:g} mm; {len(triangles)} triangles; closed mesh; outward winding; volume {volume:g} mm³")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--length", type=positive, default=400.0)
    parser.add_argument("--width", type=positive, default=300.0)
    parser.add_argument("--thickness", type=positive, default=3.5)
    args = parser.parse_args()
    try:
        verify(args.path, (args.length, args.width, args.thickness))
    except (OSError, ValueError, struct.error) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
