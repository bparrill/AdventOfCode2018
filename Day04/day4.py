# Advent of code - Day Four

import re

import pandas as pd

# Read data file, slit lines into a list
with open('input.txt', 'r') as f:
    strData = f.read().split('\n')

# Build a list of all the areas covered
# [1518-05-04 23:56] Guard #523 begins shift
eventList = []
for row in strData:
    match = re.match(r'\[(?P<date>.+) (?P<time>.+)\] (?P<event>.*)', row)
    if match != None:
        eventList.append(match.groupdict())

df = pd.DataFrame(eventList)
df.sort_values(['date', 'time'], inplace=True)
df.reset_index(drop=True, inplace=True)

# Add a guard column so we can keep track of which guard the record refers to
# The first pass looks for 'begins shift' entries and sets the guard number
def findGuard(s):
    match = re.search(r'#(?P<guard>\d+)', s)
    if match is not None:
        guard = match.group('guard')
    else:
        guard = None
    return guard

df['guard'] = df['event'].apply(findGuard)
# Fill empty guard values
df['guard'] = df['guard'].fillna(method='ffill')

# Create a status column showing awake/asleep
def setStatus(s):
    if s == 'falls asleep':
        status = 'asleep'
    elif s == 'wakes up':
        status = 'awake'
    elif 'begins shift' in s:
        status = 'awake'
    return status
df['status'] = df['event'].apply(setStatus)

# Convert hours:minutes to just minutes
df['minute'] = df['time'].apply(lambda s: int(s[0:2]) * 60 + int(s[3:5]))

# Let's enlarge the dataframe so each row covers a minute time span
new_index = pd.Index([x for x in range(60*24)], name='minute')
dfAll = pd.DataFrame(columns=df.columns)
for name, group in df.groupby('date'):
    group = group.set_index('minute').reindex(new_index).reset_index()
    dfAll = dfAll.append(group, ignore_index=True, sort=False)

# Fill in the rest of the times based on the row above
for i in range(1, len(dfAll)):
    if dfAll.iat[i, 4] == '':
        dfAll.iat[i,4] = dfAll.iat[i-1,4]

# Fill rows with column above
dfAll['date']   = dfAll['date'].fillna(method='ffill')
dfAll['guard']  = dfAll['guard'].fillna(method='ffill')
dfAll['status'] = dfAll['status'].fillna(method='ffill')

# We only care about the time when the guard is asleep
dfAsleep = dfAll[dfAll['status'] == 'asleep']
dfAsleep = dfAsleep.drop(['event', 'time', 'status'], axis=1)

mostAsleep = dfAsleep.groupby('guard')['minute'].count().idxmax()
print(f"Guard with most time asleep: {mostAsleep}")

# Find the minute of the day they were most likely asleep
minuteAsleep = dfAsleep[dfAsleep['guard'] == mostAsleep]['minute'].value_counts().idxmax()
print(f'Minute guard is most likely sleep: {minuteAsleep}')

# Calculate the value needed to enter answer:
print(f'{mostAsleep} * {minuteAsleep} = {int(mostAsleep)*int(minuteAsleep)}')

# Part 2
dfPivot = pd.pivot_table(dfAsleep[['guard', 'minute']].reset_index(drop=True), index='minute', columns='guard', aggfunc=len, fill_value=0)
dfPivot.reset_index(drop=True, inplace=True)

# Find the guard with the maximum number of times asleep for a minute
guardAsleep = dfPivot.max().idxmax()
guardAsleepMinute = dfPivot[guardAsleep].idxmax()
print(f'{guardAsleep} * {guardAsleepMinute} = {int(guardAsleep)*guardAsleepMinute}')
