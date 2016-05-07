def getNextNumber(number):
    result = None
    if number % 2 == 0:
        result = number / 2
    else:
        result = number * 3 + 1
    return result

def printNumberSequence(start, showSeq=True):
    cycleLength = 1
    while start != 1:
        if showSeq: print start, ' ',
        start = getNextNumber(start)   # Assume 1 returned eventually
        cycleLength += 1
    if showSeq: print 1, ' cycle=', cycleLength
    return cycleLength

def getMaxCycleLength(start, end, showSeq=False):
    maxCycleLength = -1
    for i in xrange(start, end+1):
        cycleLength = printNumberSequence(i, showSeq)
        if cycleLength > maxCycleLength:
            maxCycleLength = cycleLength
    return maxCycleLength

if __name__ == '__main__':
    showSeq=False

    start, end = 1, 10
    print start, end, getMaxCycleLength(start, end, showSeq)

    start, end = 100, 200
    print start, end, getMaxCycleLength(start, end, showSeq)

    start, end = 201, 210
    print start, end, getMaxCycleLength(start, end, showSeq)

    start, end = 900, 1000
    print start, end, getMaxCycleLength(start, end, showSeq)