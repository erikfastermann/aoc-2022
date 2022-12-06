from pathlib import Path

datastream = Path('input.txt').read_text()

def packet_marker(n):
    for i in range(len(datastream)-n-1):
        if len(set(datastream[i:i+n])) == n:
            return i + n

print(packet_marker(4))
print(packet_marker(14))