# Advent of code - Day one

# Read data file, slit lines into a list
with open('input.txt', 'r') as f:
    data = f.read().split()

# Convert list of strings to integer, then add them all up
print(f'Resulting frequency is: {sum([int(i) for i in data])}')
