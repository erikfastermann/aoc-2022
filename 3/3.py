from pathlib import Path
import string
import itertools

rucksacks = Path('input.txt').read_text().strip().split('\n')

def calculate_priorities():
    lower = zip(string.ascii_lowercase, itertools.count(1))
    upper = zip(string.ascii_uppercase, itertools.count(27))
    return {item: prio for item, prio in itertools.chain(lower, upper)}

priority = calculate_priorities()

def find_duplicate(first, *others):
    others = [set(other) for other in others]
    for item in first:
        found = 0
        for other in others:
            if item in other:
                found += 1
        if found == len(others):
            return item
    assert False

def generate_1():
    for rucksack in rucksacks:
        c1 = rucksack[:len(rucksack)//2]
        c2 = rucksack[len(rucksack)//2:]
        item = find_duplicate(c1, c2)
        yield priority[item]

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def generate_2():
    for group in chunks(rucksacks, 3):
        item = find_duplicate(*group)
        yield priority[item]

print(sum(generate_1()))
print(sum(generate_2()))