# Advent of code - Day Six
# Note: addressing of nparray is (row, column) which correlates to (y,x)

import array

import numpy as np

# Read data file, slit lines into a list
with open('input.txt', 'r') as f:
    strData = f.read().strip().replace(' ', '').split('\n')

# Convert to list of lists with integers
posData = [[int(y) for y in x] for x in [i.split(',') for i in strData]]

maxX = 0
maxY = 0
minX = 1000
minY = 1000

for x,y in posData:
    if x < minX: minX = x
    if x > maxX: maxX = x
    if y < minY: minY = y
    if y > maxY: maxY = y


# Returns 'manhattan' distance between the two points
def distance(p1, p2):
    d = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    return d

# Takes a list and returns the index of the minimum distance
# If multiples are found then -1 is returned
def minDistance(l):
    minValue = min(l)
    minList = [x for x in l if x == minValue]
    if len(minList) > 1: idx = -1
    else: idx = l.index(minValue)
    return idx

# Create our field
field = np.full([maxY+1, maxX+1], -2)

# For each field point, calculate closest point
it = np.nditer(field, flags=['multi_index'])
while not it.finished:
    dist = [distance([it.multi_index[1],it.multi_index[0]], pos) for pos in posData]
    field[it.multi_index] = minDistance(dist)
    n = it.iternext()

# Get infinite values by looking on outer edges
infList = set(field[0])           # Top row
infList.update(field[:][0])       # Left column
infList.update(field[-1])     # Bottom row
infList.update(field[:][-1])  # Right column

# Collapse array into giant list and remove infinite list elements
fieldList = list(field.flatten())

reducedList = [x for x in fieldList if x not in infList]

# For each of the remaining entries, determine which one has the most positions
idxList = list(set(reducedList))
areas   = {}
for i in idxList:
    areas[i] = len([el for el in reducedList if el == i])

maxArea = max(areas, key=areas.get)
print(f'maximum area is {maxArea} with {areas[maxArea]} units.')

# Part two
# For each field point, calculate sum of distances to each point
areaSize = 0
it = np.nditer(field, flags=['multi_index'])
while not it.finished:
    if sum([distance([it.multi_index[1],it.multi_index[0]], pos) for pos in posData]) < 10000:
        areaSize += 1
    n = it.iternext()

print(f'Area size of safe zone within 10,000 of all points: {areaSize}')