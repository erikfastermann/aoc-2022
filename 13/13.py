from pathlib import Path
import re
import functools
import itertools

packets_raw = Path('input.txt').read_text().strip()

def parse():
    p = re.sub('^$', '],[', packets_raw, flags=re.MULTILINE)
    p = re.sub('\]$', '],', p, flags=re.MULTILINE)
    return eval(f'[[{p}]]') # unsafe for untrusted input

packets = parse()

def compare_int(x, y):
    return (x > y) - (x < y)

def compare(a, b):
    for x, y in zip(a, b):
        match (isinstance(x, list), isinstance(y, list)):
            case (False, False):
                result = compare_int(x, y)
            case (True, False):
                result = compare(x, [y])
            case (False, True):
                result = compare([x], y)
            case (True, True):
                result = compare(x, y)
        if result < 0 or result > 0:
            return result
    return compare_int(len(a), len(b))

def sum_sorted_index_pairs():
    return sum(i + 1 for i, (a, b) in enumerate(packets) if compare(a, b) <= 0)

def flatten():
    return (packet for pair in packets for packet in pair)

DIVIDER_PACKETS = [[[2]], [[6]]]

def get_decoder_key():
    packets = list(itertools.chain(DIVIDER_PACKETS, flatten()))
    packets.sort(key=functools.cmp_to_key(compare))
    i1 = packets.index(DIVIDER_PACKETS[0])
    i2 = packets.index(DIVIDER_PACKETS[1])
    return (i1 + 1) * (i2 + 1)

print(sum_sorted_index_pairs())
print(get_decoder_key())