from pathlib import Path

motions_raw = Path('input.txt').read_text().splitlines()

def parse_motions():
    for direction_and_steps in motions_raw:
        direction, steps_raw = direction_and_steps.split()
        steps = int(steps_raw)
        yield (direction, steps)

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

def cmp(a, b):
    return (a > b) - (a < b)

def move_tail(tail, head):
    x = cmp(head[0], tail[0])
    y = cmp(head[1], tail[1])
    return (tail[0] + x, tail[1] + y)

def simulate_step(knots, direction):
    knots[0] = move(knots[0], direction)
    for i in range(1, len(knots)):
        if not is_touching(knots[i], knots[i-1]):
            knots[i] = move_tail(knots[i], knots[i-1])
            assert is_touching(knots[i], knots[i-1])
        else:
            break

def simulate(n):
    assert n >= 2
    knots = [(0, 0)] * n
    yield (0, 0)
    for direction, steps in motions:
        for _ in range(steps):
            old_tail = knots[-1]
            simulate_step(knots, direction)
            if knots[-1] != old_tail:
                yield knots[-1]

print(len(set(simulate(2))))
print(len(set(simulate(10))))