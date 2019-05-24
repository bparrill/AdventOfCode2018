import time

# Part one
# Read data file, slit lines into a list
with open('input.txt', 'r') as f:
    strData = f.read().strip().split('\n')

stepsList = []
for step in strData:
    stepsList.append([step[5], step[36]])

# Store in dictionary
steps = {}
for step in stepsList:
    #print(f'Processing: {step[0]} -> {step[1]}')
    # Add the 1st step to dictionary if it doesn't already exist
    steps.setdefault(step[0], [])
    # Add the 2nd step to the dictionary if it doesn't already exist
    # Add the 1st step as the value, keep in the list to show which 
    # keys the value must come after
    steps.setdefault(step[1], []).append(step[0])
    #print(steps)

#print(steps)

order = []
while steps.keys():
    # Empty list for dictionary value means these items come next.  Sort in alphabetical
    # order and take the first from the list
    next = sorted([key for key, value in steps.items() if value == []])[0]
    # Append the key to the order and delete once added
    order.append(next)
    del steps[next]
    # Remove the key from all values
    dependencies = [key for key, value in steps.items() if next in value]
    for dependency in dependencies:
        steps[dependency].remove(next)

answer = ''.join(order)
print(f'Sequence of steps: {answer}')

# Part two
def taskTime(c):
    # Time it takes to do a task = 60 + A=1, B=2, etc
    return 60 + (ord(c) - ord('A') + 1)

# Build dependency list again
for step in stepsList:
    steps.setdefault(step[0], [])
    steps.setdefault(step[1], []).append(step[0])

seconds = 0
#finish  = [0, 0]
finish  = [0, 0, 0, 0, 0]
process = {}

while steps.keys():
    readyTasks = sorted([key for key, value in steps.items() if value == []])
    elapsedTime = 0
    for readyTask in readyTasks:
        # Assign the task to the first idle worker
        # Be sure it's not already being worked on 
        if (0 in finish) and (readyTask not in list(process.keys())):
            readyWorker = finish.index(0)
            finish[readyWorker]  = taskTime(readyTask) + seconds
            print(f'Task {readyTask} assigned at time {seconds} to worker {readyWorker} done at {finish[readyWorker]}')
            process[readyTask] = finish[readyWorker]
            elapsedTime = taskTime(readyTask) if elapsedTime == 0 else min([elapsedTime, taskTime(readyTask)])
        else:
            elapsedTime = 1

    # All work has been assigned, now deal with the time
    # The task with the lowest amount of time will complete first
    seconds += elapsedTime
    #print(f'Time update: added {elapsedTime} - {seconds}')
    #print(f'Time is now {seconds}')
    # Remove the task from the list if the time will be passed
    # k is the step (letter) to remove
    # v is the target finish time
    delList = []
    #print(f'Processing at time {seconds} - {process}')
    for k, v in process.items():
        if v <= seconds:
            del steps[k]
            delList.append(k)
            dependencies = [key for key, value in steps.items() if k in value]
            for dependency in dependencies:
                steps[dependency].remove(k)
            #print(f'Deleted step {k} - Steps: {steps} Process: {process} Delete: {delList}')
    for key in delList:
        #print(f'Deleting process for step {key} - {process}')
        del process[key]
    # Subtract the time from all the workers to account for elapsed time
    finish = [x if x > seconds else 0 for x in finish]
    #time.sleep(3)

# At the end, the longest task time will be our finish time
#seconds += max(working)
print(f'Total time: {seconds} seconds')

