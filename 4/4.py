from pathlib import Path

pairs = Path('input.txt').read_text().strip().split('\n')

def as_range(s):
    a, b = s.split('-')
    return (int(a), int(b))

def extract_ranges():
    for pair in pairs:
        a, b = pair.split(',')
        yield (as_range(a), as_range(b))

ranges = list(extract_ranges())

def is_inside(a, b):
    return a[0] >= b[0] and a[1] <= b[1]

def does_overlap(a, b):
    return a[1] >= b[0] and a[0] <= b[1]

count_1 = sum(is_inside(a, b) or is_inside(b, a) for a, b in ranges)
count_2 = sum(does_overlap(a, b) or does_overlap(b, a) for a, b in ranges)
print(count_1)
print(count_2)