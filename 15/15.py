import re
from types import SimpleNamespace
from dataclasses import dataclass
from pathlib import Path

positions_raw = [
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
    'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
    'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
    'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
    'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
    'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
    'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
    'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
    'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
    'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
    'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
    'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
    'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
    'Sensor at x=20, y=1: closest beacon is at x=15, y=3',
]
positions_raw = Path('input.txt').read_text().splitlines()

@dataclass
class Position:
    x: int
    y: int

def parse():
    for position in positions_raw:
        pattern = '^[^\d\-]*(-?\d+)[^\d\-]*(-?\d+)[^\d\-]*(-?\d+)[^\d\-]*(-?\d+)$'
        match = re.search(pattern, position)
        sensor = Position(int(match[1]), int(match[2]))
        beacon = Position(int(match[3]), int(match[4]))
        yield SimpleNamespace(sensor=sensor, beacon=beacon)

positions = list(parse())

def manhatten_distance(sensor, beacon):
    return abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)

def all_positions_for_row(sensor, absolute_distance, row):
    y_range = range(sensor.y - absolute_distance, sensor.y + absolute_distance + 1)
    if row in y_range:
        d = max(sensor.y, row) - min(sensor.y, row)
        r = absolute_distance - d
        for x in range(-r, r+1):
            yield Position(sensor.x + x, row)

def start_and_row_length():
    start = min(p.beacon.x for p in positions)
    last = max(p.beacon.x for p in positions)
    return (start, last - start)

def row(n):
    start, row_length = start_and_row_length()
    row = [False] * row_length
    for p in positions:
        d = abs(manhatten_distance(p.sensor, p.beacon))
        for found in all_positions_for_row(p.sensor, d, n):
            if found == p.sensor or found == p.beacon:
                continue
            row[abs(start) + found.x] = True
    return sum(1 for field in row if field is True)

print(row(2_000_000))