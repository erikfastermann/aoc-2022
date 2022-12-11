from pathlib import Path
from itertools import groupby
import copy

monkeys_raw = Path('input_test.txt').read_text().splitlines()

def split(lines):
    return (list(group) for k, group in groupby(lines, lambda x: x == '') if not k)

def parse():
    for i, monkey_raw in enumerate(split(monkeys_raw)):
        op_raw = ' '.join(monkey_raw[2].split()[-3:])
        items_raw = monkey_raw[1].split(':')[1].strip().split(', ')
        monkey = {
            'items': [int(item) for item in items_raw],
            'op': eval(f'lambda old: {op_raw}'),
            'divisible_test': int(monkey_raw[3].split()[-1]),
            'throw_true': int(monkey_raw[4].split()[-1]),
            'throw_false': int(monkey_raw[5].split()[-1]),
            'inspected_count': 0,
        }
        yield monkey

monkeys = list(parse())

def round(monkeys, decrease_worry_level):
    for monkey in monkeys:
        for item in monkey['items']:
            new_worry_level = monkey['op'](item)
            if decrease_worry_level:
                new_worry_level //= 3
            if new_worry_level%monkey['divisible_test'] == 0:
                monkeys[monkey['throw_true']]['items'].append(new_worry_level)
            else:
                monkeys[monkey['throw_false']]['items'].append(new_worry_level)
        monkey['inspected_count'] += len(monkey['items'])
        monkey['items'].clear()

def monkey_business(rounds, decrease_worry_level):
    my_monkeys = copy.deepcopy(monkeys)
    for i in range(rounds):
        print(i)
        round(my_monkeys, decrease_worry_level)
    my_monkeys.sort(key=lambda x: x['inspected_count'], reverse=True)
    return my_monkeys[0]['inspected_count'] * my_monkeys[1]['inspected_count']

print(monkey_business(20, True))
print(monkey_business(10000, False))