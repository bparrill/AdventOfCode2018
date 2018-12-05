# Advent of code - Day Three

import re

import pandas as pd

# Read data file, slit lines into a list
with open('input.txt', 'r') as f:
    strData = f.read().split('\n')

# Build a list of all the areas covered
claimList = []
for claimID in strData:
    match = re.match(r'#(?P<IDNum>\d+) @ (?P<edgeL>\d+),(?P<edgeT>\d+): (?P<width>\d+)x(?P<height>\d+)', claimID)
    if match != None:
        claimList.append(match.groupdict())

# Create a dataframe with our list, then convert everything to integer
df = pd.DataFrame(claimList).astype(int)

# Determine the maximum width and height of our claimed cloth, then make a giant array to hold each square inch
bottom = max(df['edgeT'] + df['height'])
right  = max(df['edgeL'] + df['width'])

# We'll use a dictionary to store each location's owner(s).  The key will be a (row, col) touple, and the
# value will be a list of owners
cloth = {}
for i, claimID in df.iterrows():
    for row in range(claimID['edgeT'], claimID['edgeT']+claimID['height']):
        for col in range(claimID['edgeL'], claimID['edgeL']+claimID['width']):
            key = (row, col)
            if key in cloth:
                cloth[key].append(claimID['IDNum'])
            else:
                cloth[key] = [claimID['IDNum']]

numOver = 0
for i in cloth.values():
    numOver += (1 if len(i) > 1 else 0)

print(f'Square inches with 2 or more claims: {numOver}')

# Part Two

# Build a list of all claims, then delete them as we find duplicates
claimList = df['IDNum'].tolist()
for i in cloth.values():
    if len(i) > 1:
        for j in i:
            if j in claimList:
                claimList.remove(j)

print(f'Remaining IDs: {claimList}')