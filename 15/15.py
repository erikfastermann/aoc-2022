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
#positions_raw = Path('input.txt').read_text().splitlines()

@dataclass(frozen=True)
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

def row_ranges(sensor, absolute_distance):
    for y in range(-absolute_distance, absolute_distance + 1):
        r = absolute_distance - abs(y)
        yield (range(sensor.x - r, sensor.x + r + 1), sensor.y + y)

def start_and_row_count():
    start = min(p.beacon.y for p in positions)
    last = max(p.beacon.y for p in positions)
    return (start, last - start + 1)

def all_row_ranges():
    start, row_count = start_and_row_count()
    rows = [[] for _ in range(row_count)]
    for p in positions:
        d = abs(manhatten_distance(p.sensor, p.beacon))
        for x_range, y in row_ranges(p.sensor, d):
            idx = abs(start) + y
            if idx >= len(rows):
                break
            rows[idx].append(x_range)
    return (start, rows)

def ranges_contain_not(ranges, v):
    return all(v not in r for r in ranges)

def not_in_ranges(ranges):
    for r in ranges:
        x = r.start - 1
        if ranges_contain_not(ranges, x):
            yield x
        x = r.stop
        if ranges_contain_not(ranges, x):
            yield x

all_known_positions = set(p for p2 in positions for p in (p2.sensor, p2.beacon))

def valid_position(ranges, lowest, highest, y):
    for x in not_in_ranges(ranges):
        if x < lowest or x > highest:
            continue
        p = Position(x, y)
        if p in all_known_positions:
            continue
        return p

def find_beacon(lowest, highest):
    start, rows = all_row_ranges()
    for y in range(lowest, highest + 1):
        idx = abs(start) + y
        if idx >= len(rows):
            break
        row = rows[idx]
        p = valid_position(row, lowest, highest, y)
        if p is not None:
            return p
    raise RuntimeError()

print(find_beacon(0, 20))
#print(find_beacon(0, 4_000_000))