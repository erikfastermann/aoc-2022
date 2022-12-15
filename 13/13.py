from pathlib import Path
import itertools
import json
import functools

packets_raw = Path('input.txt').read_text().splitlines()

def separated_by_newline():
    grouped = itertools.groupby(packets_raw, lambda x: x == '')
    return (packets for k, packets in grouped if not k)

def parse():
    for pair in separated_by_newline():
        yield [json.loads(packet) for packet in pair]

packets = list(parse())

def compare_int(x, y):
    return (x > y) - (x < y)

def compare_list(x, y):
    match (isinstance(x, list), isinstance(y, list)):
        case (False, False):
            return compare_int(x, y)
        case (True, False):
            return compare(x, [y])
        case (False, True):
            return compare([x], y)
        case (True, True):
            return compare(x, y)

def compare(a, b):
    for x, y in zip(a, b):
        result = compare_list(x, y)
        if result != 0:
            return result
    return compare_int(len(a), len(b))

def sum_sorted_index_pairs():
    return sum(i + 1 for i, (a, b) in enumerate(packets) if compare(a, b) <= 0)

def flatten():
    return (packet for pair in packets for packet in pair)

DIVIDER_PACKETS = [[[2]], [[6]]]

def binary_search(lst, v):
    low = 0
    high = len(lst) - 1
    while low <= high:
        mid = low + (high - low)//2
        match compare(lst[mid], v):
            case 0:
                return mid
            case -1:
                low = mid + 1
            case 1:
                high = mid - 1
            case _:
                raise ValueError()
    raise RuntimeError()

def get_decoder_key():
    packets = list(itertools.chain(DIVIDER_PACKETS, flatten()))
    packets.sort(key=functools.cmp_to_key(compare))
    i1 = binary_search(packets, DIVIDER_PACKETS[0])
    i2 = binary_search(packets, DIVIDER_PACKETS[1])
    return (i1 + 1) * (i2 + 1)

print(sum_sorted_index_pairs())
print(get_decoder_key())