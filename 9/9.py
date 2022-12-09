from pathlib import Path

motions_raw = [
    'R 4',
    'U 4',
    'L 3',
    'D 1',
    'R 4',
    'D 1',
    'L 5',
    'R 2',
]
motions_raw = Path('input.txt').read_text().splitlines()

def parse_motions():
    for direction_and_count in motions_raw:
        direction, count_raw = direction_and_count.split()
        count = int(count_raw)
        yield (direction, count)

motions = list(parse_motions())

def move(position, direction):
    match direction:
        case 'R':
            return (position[0] + 1, position[1])
        case 'L':
            return (position[0] - 1, position[1])
        case 'U':
            return (position[0], position[1] + 1)
        case 'D':
            return (position[0], position[1] - 1)
        case _:
            raise RuntimeError()

def is_touching(tail, head):
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (tail[0] + x, tail[1] + y) == head:
                return True
    return False

def simulate():
    head = (0, 0)
    tail = (0, 0)
    yield tail
    for direction, count in motions:
        for _ in range(count):
            next_head = move(head, direction)
            if not is_touching(tail, next_head):
                tail = head
                yield tail
            head = next_head

def simulate_many(n):
    knots = [(0, 0)] * n
    yield (0, 0)
    for direction, count in motions:
        for _ in range(count):
            next_position = move(knots[0], direction)
            for i in range(1, len(knots)):
                if not is_touching(knots[i], knots[i-1]):
                    knots[i] = knots[i-1]
                    # TODO

print(len(set(simulate())))