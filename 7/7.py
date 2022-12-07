from pathlib import Path

terminal = Path('input.txt').read_text().strip().split('\n')

def parse(i):
    current = {}
    while i < len(terminal):
        line = terminal[i]
        i += 1
        match line.split():
            case ['$', 'cd', '..']:
                return (current, i)
            case ['$', 'cd', d]:
                child, i = parse(i)
                current[d] = child
            case ['$', 'ls']:
                pass
            case ['dir', d]:
                pass
            case [size, f]:
                current[f] = int(size)
    return (current, i)

MAX_SIZE = 100_000
AVAILABLE_SPACE = 70_000_000
REQUIRED_SPACE = 30_000_000

def directories_size(d):
    current_size = 0
    for size_or_next_dir in d.values():
        if isinstance(size_or_next_dir, int):
            current_size += size_or_next_dir
        else:
            size = yield from directories_size(size_or_next_dir)
            current_size += size
    yield current_size
    return current_size

tree = parse(0)[0]

def large_directories_size():
    return sum(s for s in directories_size(tree) if s <= MAX_SIZE)

def delete_directory_size():
    root_size = max(directories_size(tree))
    atleast_delete = REQUIRED_SPACE - (AVAILABLE_SPACE - root_size)
    return min(s for s in directories_size(tree) if s >= atleast_delete)

print(large_directories_size())
print(delete_directory_size())