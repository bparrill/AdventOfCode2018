# Advent of code - Day Five

# Read data file, slit lines into a list
with open('input.txt', 'r', newline='') as f:
    strData = f.read().strip()

saveStr = strData

# Finds a match and returns the postion, otherwise returns -1 if no match
def findMatch(s, start):
    i = start
    found = False
    while (i < len(s)-1) and not found:
        #print(f'Comparing "{s[i]}" to "{s[i+1]}"')
        # Look for UPPER / lower combo
        if s[i].isupper() and s[i+1].islower() and (s[i+1].upper() == s[i].upper()):
            found = True
        # Look for lower / UPPER combo
        elif s[i+1].isupper() and s[i].islower() and (s[i+1].upper() == s[i].upper()):
            found = True
        else:
            i += 1
    if not found:
        i = -1
    return i

def react(strData):
    iteration = 0
    print(f'Iteration: ', end='', flush=True)
    while findMatch(strData, 0) >= 0:
        done = False
        if (iteration % 50) == 0:
            print(f'{iteration}.', end='', flush=True)
        pos = 0
        newData = ''
        while (pos < (len(strData)-1)) and not done:
            matchPos = findMatch(strData, pos)
            if matchPos == -1:
                done = True
                newData = newData + strData[pos:]
            else:
                newData = newData + strData[pos:matchPos]
                #print(f'Match at {matchPos}: {strData}/{newData}')
                pos = matchPos + 2
                #print(f'pos is now {pos}')
        #print(f'Final string: {newData}')
        strData = newData
        iteration += 1
    print(f'\nTotal iterations: {iteration}')
    return strData

strData = react(strData)
print(f'Length of resulting polymer: {len(strData)}')

# Part two
lengths = {}
strData = saveStr

# Get a list of all letters regardless of case
letters = list(set(strData.upper()))
#letters = []

#Run through the process above for each letter, recording the output
for letter in letters:
    print(f'Testing {letter}')
    # Remove the upper and lowercase letters
    testStr = saveStr.replace(letter, '')
    testStr = testStr.replace(letter.lower(), '')
    strData = react(testStr)
    print(f'Length of resulting polymer: {len(strData)}')
    lengths[letter] = len(strData)

print(lengths)
print(f'Minimum length: {min(lengths.values())} by removing the letter: {min(lengths, key=lengths.get)}')