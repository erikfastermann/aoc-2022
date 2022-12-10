from pathlib import Path

program = Path('input.txt').read_text().splitlines()

def execute():
    x = 1
    cycle = 0
    for instruction in program:
        match instruction.split():
            case ['noop']:
                yield (cycle + 1, x)
                cycle += 1
            case ['addx', n]:
                yield (cycle + 1, x)
                yield (cycle + 2, x)
                x += int(n)
                cycle += 2
            case _:
                raise ValueError()

INTERESTING_CYCLES = [20, 60, 100, 140, 180, 220]

def interesting_signal_strengths():
    return (cycle * x for cycle, x in execute() if cycle in INTERESTING_CYCLES)

def draw_screen():
    beam = 0
    row = []
    for _, x in execute():
        if x-1 <= beam <= x+1:
            row.append('#')
        else:
            row.append('.')
        beam = (beam + 1) % 40
        if beam == 0:
            print(''.join(row))
            row = []

print(sum(interesting_signal_strengths()))
draw_screen()