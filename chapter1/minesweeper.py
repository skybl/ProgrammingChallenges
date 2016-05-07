def processField(fieldArray, rows, cols, show=False):
    # Check dimensions
    if (not 0 < rows <= 100) or (not 0 < cols <= 100):
        raise Exception('Invalid rows %d cols %d'%(rows, cols))
    if len(fieldArray) != rows or len(fieldArray[0]) != cols:
        raise Exception('Stated dimensions do not match actual ones')

    if rows == 0 and cols == 0:
        return

    for i,line in enumerate(fieldArray):
        for j,char in enumerate(line):

            if char != '*':  # and i == 1 and j == 0:
                if char == '.':
                    numMines = 0

                    # Look for immediately neighbouring mines
                    startRowIndex = i - 1
                    if startRowIndex < 0:
                        startRowIndex = 0
                    endRowIndex = i + 1
                    if endRowIndex > rows:
                        endRowIndex = rows

                    for localLine in fieldArray[startRowIndex:endRowIndex+1]:

                        startColIndex = j - 1
                        if startColIndex < 0:
                            startColIndex = 0
                        endColIndex = j + 1
                        if endColIndex > cols:
                            endColIndex = cols

                        for c in localLine[startColIndex:endColIndex + 1]:
                            if c == '*':
                                numMines += 1
                    print numMines,
                else:
                    raise Exception('Invalid character encountered %c'%(char))
            else:
                print '*',
        print

if __name__ == '__main__':
    num = 1
    rows, cols = 4, 4
    field = [
        '*...',
        '....',
        '.*..',
        '....'
    ]
    print 'Field #%d:'%num
    processField(field, rows, cols)
    print

    num += 1

    rows, cols = 3, 5
    field = [
        '**...',
        '.....',
        '.*...'
    ]
    print 'Field #%d:'%num
    processField(field, rows, cols)
    print
