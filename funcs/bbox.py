import math
import sys
from dataclasses import dataclass


@dataclass  
class BoundingBox:
    north: float
    south: float
    east: float
    west: float


def tile_bbox(zoom: int, x: int, y: int) -> BoundingBox:
    return BoundingBox(
        north=tile_lat(y, zoom),
        south=tile_lat(y + 1, zoom),
        west=tile_lon(x, zoom),
        east=tile_lon(x + 1, zoom),
    )


def tile_lon(x: int, z: int) -> float:
    return x / math.pow(2.0, z) * 360.0 - 180


def tile_lat(y: int, z: int) -> float:
    return math.degrees(
        math.atan(math.sinh(math.pi - (2.0 * math.pi * y) / math.pow(2.0, z)))
    )


if __name__ == "__main__":
    bbox = tile_bbox(*map(int, sys.argv[1].split("/")))
    print(
        f"ST_MakeEnvelope({bbox.west}, {bbox.south}, {bbox.east}, {bbox.north}, 4326)"
    )