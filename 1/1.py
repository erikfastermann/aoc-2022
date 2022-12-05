from pathlib import Path
from itertools import groupby

lines = Path('input.txt').read_text().split('\n')
chunks = (numbers for k, numbers in groupby(lines, lambda x: x == '') if not k)
result = sorted(sum(int(n) for n in numbers) for numbers in chunks)
print("largest:", result[-1])
print("top three:", sum(result[-3:]))