digit0 = [
    ' _ ',
    '| |',
    '   ',
    '| |',
    ' _ '
]

digit1 = [
    '   ',
    ' | ',
    '   ',
    ' | ',
    '   '
]

digit2 = [
    ' _ ',
    '  |',
    ' _ ',
    '|  ',
    ' _ '
]

digit3 = [
    ' _ ',
    '  |',
    ' _ ',
    '  |',
    ' _ '
]

digit4 = [
    '   ',
    '| |',
    ' _ ',
    '  |',
    '  '
]

digit5 = [
    ' _ ',
    '|  ',
    ' _ ',
    '  |',
    ' _ '
]

digit6 = [
    ' _ ',
    '|  ',
    ' _ ',
    '| |',
    ' _ '
]

digit7 = [
    ' _ ',
    '  |',
    '   ',
    '  |',
    '   '
]

digit8 = [
    ' _ ',
    '| |',
    ' _ ',
    '| |',
    ' _ '
]

digit9 = [
    ' _ ',
    '| |',
    ' _ ',
    '  |',
    ' _ '
]

# s + 2 columns and 2s+3 rows
def addSpaceToDigitLines(digitLines):
    newDigitLines = []
    for line in digitLines:
        newDigitLines.append(line+' ')
    return newDigitLines

def convertCharArrayToString(charArray):
    newString = ''
    for c in charArray:
        newString += c
    return newString

def enlargenDigit(digitLines, digitSize):
    # NB: Each line contains '_' or '|' characters exclusively, possibly along with spaces
    newLines = []
    newLineSize = digitSize + 2
    for line in digitLines:
        newLine = ''

        # Handle columns
        if line.find('_') > -1:
            for c in line:
                if c == ' ':
                    newLine += ' '
                elif c == '_':
                    for i in xrange(digitSize):
                        newLine += '_'
            newLines.append(newLine)

        # Handle rows
        elif line.find('|') > -1:
            # Fatten line
            charArray = []   # Like mutable string
            for i in xrange(newLineSize):
                charArray += ' '

            if line[0] == ' ' and line[1] == '|' and line[2] == ' ':
                charArray[len(charArray)/2] = '|'
            if line[0] == '|' and line[1] == ' ' and line[2] == '|':
                charArray[0] = '|'
                charArray[len(charArray)-1] = '|'
            if line[0] == ' ' and line[1] == ' ' and line[2] == '|':
                charArray[len(charArray)-1] = '|'
            if line[0] == '|' and line[1] == ' ' and line[2] == ' ':
                charArray[0] = '|'

            newLine = convertCharArrayToString(charArray)

            # Make copies across rows
            for i in xrange(digitSize):
                newLines.append(newLine)

        elif line.find(' ') > -1:
            for i in xrange(newLineSize):
                newLine += ' '
            newLines.append(newLine)

        else:
            raise Exception('Invalid character found '%(line))

    return newLines

def display(digitSize, num):
    lines = []

    string = str(num)
    for c in string:
        # Digits enumeration
        if c == '0':
            newLines = enlargenDigit(digit0, digitSize)
        elif c == '1':
            newLines = enlargenDigit(digit1, digitSize)
        elif c == '2':
            newLines = enlargenDigit(digit2, digitSize)
        elif c == '3':
            newLines = enlargenDigit(digit3, digitSize)
        elif c == '4':
            newLines = enlargenDigit(digit4, digitSize)
        elif c == '5':
            newLines = enlargenDigit(digit5, digitSize)
        elif c == '6':
            newLines = enlargenDigit(digit6, digitSize)
        elif c == '7':
            newLines = enlargenDigit(digit7, digitSize)
        elif c == '8':
            newLines = enlargenDigit(digit8, digitSize)
        elif c == '9':
            newLines = enlargenDigit(digit9, digitSize)
        else:
            raise Exception('Do not recognise digit '%(c))

        # Concatenate new lines
        if len(lines) == 0:
            for line in newLines:
                lines.append(line)
        else:
            tempLines = []
            for line, newLine in zip(lines, newLines):
                tempLines.append(line + newLine)
            lines = tempLines

        lines = addSpaceToDigitLines(lines)

    for line in lines:
        print line

if __name__ == '__main__':


    s, n = 2, 12345
    display(s, n)

    s, n = 3, 67890
    display(s, n)

    s, n = 0, 0
    display(s, n)
