# Advent of code - Day Two

import collections

# Read data file, slit lines into a list
with open('input.txt', 'r') as f:
    strData = f.read().split()

# Keep track of how many entries have exactly 2 and exactly 3 letters
letters2 = 0
letters3 = 0

for i in strData:
    counter = collections.Counter(i)
    counts  = counter.values()
    letters2 = letters2 + (1 if 2 in counts else 0)
    letters3 = letters3 + (1 if 3 in counts else 0)

print(f'2 letter count: {letters2}')
print(f'3 letter count: {letters3}')
print(f'Hash: {letters2*letters3}')

# Part Two

# Returns the difference count between the two strings
def diffCount(s1, s2):
    diff = 0
    for i in range(len(s1)):
        diff += (0 if s1[i] == s2[i] else 1)
    return diff

# Start comparison against all entries after the one we're checking
pos   = 0
found = False
while not found:
    pos2 = pos + 1
    while (not found) and (pos2 < len(strData)):
        if diffCount(strData[pos], strData[pos2]) == 1:
            found = True
            box1 = strData[pos]
            box2 = strData[pos2]
        pos2 += 1
    pos += 1

print(f'Boxes which differ in only one position: {box1}, {box2}')

commonLetters = []
for i in range(len(box1)):
    if box1[i] == box2[i]:
        commonLetters.append(box1[i])

print(f'Common letters: {"".join(commonLetters)}')