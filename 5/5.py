from pathlib import Path
import re
import copy

stacks_and_arranges = Path('input.txt').read_text().rstrip().split('\n')

def split_stacks_and_arranges():
    split = stacks_and_arranges.index('')
    return (stacks_and_arranges[:split], stacks_and_arranges[split+1:])

stacks_raw, arranges_raw = split_stacks_and_arranges()

def parse_stacks():
    n = (len(stacks_raw[0])+1) // 4
    stacks = [[] for _ in range(n)]
    for row in stacks_raw[:-1]:
        for i in range(n):
            maybe_crate = row[i*4+1]
            if maybe_crate != ' ':
                stacks[i].append(maybe_crate)
    for stack in stacks:
        stack.reverse()
    return stacks

stacks = parse_stacks()

def generate_arrange():
    for arrange_raw in arranges_raw:
        arrange = re.search('^move (\d+) from (\d) to (\d)$', arrange_raw).groups()
        yield (int(arrange[0]), int(arrange[1])-1, int(arrange[2])-1)

def arrange_containers(crate_mover_9000):
    our_stacks = copy.deepcopy(stacks)
    for move, frm, to in generate_arrange():
        moved_stack = our_stacks[frm][-move:]
        if crate_mover_9000:
            moved_stack.reverse()
        our_stacks[to].extend(moved_stack)
        del our_stacks[frm][-move:]
    return our_stacks

def last_elements(ll):
    return ''.join(l[-1] for l in ll)

print(last_elements(arrange_containers(True)))
print(last_elements(arrange_containers(False)))