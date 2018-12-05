# Advent of code - Day one

# Read data file, slit lines into a list
with open('input.txt', 'r') as f:
    strData = f.read().split()

# Convert from string to int
data = [int(i) for i in strData]

# Part 1
# Convert list of strings to integer, then add them all up
print(f'Resulting frequency is: {sum(data)}')

# Part 2
# Keep a running list of frequencies, look for the first frequency it reaches twice
freqList = []
curFreq  = 0
found    = False
loops    = 0
while not found:
    for i in data:
        curFreq = curFreq + i
        if (curFreq in freqList) and (not found):
            print(f'Frequency {curFreq} has previously been reached')
            found = True
        freqList.append(curFreq)
    loops = loops + 1
    print(f'Completed {loops} loops through the data.  Frequency list at {len(freqList)} items.')
