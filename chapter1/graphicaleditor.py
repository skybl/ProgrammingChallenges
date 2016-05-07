###############################################################################
#
###############################################################################
class Session:
    def __init__(self):
        self.stack = []  # To store image instances

    def processCommand(self, command):
        cmd = command.strip().upper()
        words = cmd.split()

        image = None  # Set image context to the top of the stack
        if len(self.stack) > 0:
            image = self.stack[len(self.stack)-1]

        if words[0].startswith('I') and len(words) == 3:
            c, cols, rows = words
            image = Image(int(rows), int(cols))
            self.stack.append(image)
        elif words[0].startswith('C') and len(words) == 1:
            image.clear()
        elif words[0].startswith('L') and len(words) == 4:
            c, y, x, colour = words
            image.set(int(x)-1, int(y)-1, colour)
        elif words[0].startswith('V') and len(words) == 5:
            c, y, x1, x2, colour = words
            image.setVertical(int(x1) - 1, int(x2) - 1, int(y) - 1, colour)
        elif words[0].startswith('H') and len(words) == 5:
            c, y1, y2, x, colour = words
            image.setHorizontal(int(x) - 1, int(y1) - 1, int(y2) - 1, colour)
        elif words[0].startswith('K') and len(words) == 6:
            c, y1, x1, y2, x2, colour = words
            image.setRectangle(int(x1) - 1, int(y1) - 1, int(x2) - 1, int(y2) - 1, colour)
        elif words[0].startswith('F') and len(words) == 4:
            c, y,x, newColour = words
            oldColour = image.array[int(x)-1][int(y)-1]
            image.fillRegion(int(x)-1, int(y)-1, oldColour, newColour)
        elif words[0].startswith('S') and len(words) == 2:
            c, nm = words
            image.setName(nm)
            print command.split()[1]
            image.show()
        elif words[0].startswith('X') and len(words) == 1:  # Terminate image context
            self.stack.pop()

###############################################################################
#
###############################################################################
class Image:
    def __init__(self, rows, cols, val=0):
        self.rows = rows
        self.cols = cols
        self.array = []
        for i in xrange(rows):
            newArray = []
            for i in xrange(cols):
                newArray.append(0)
            self.array.append(newArray)
        self.name = None

    def set(self, i, j, val):
        self.array[i][j] = val

    def setVertical(self, i1,i2,j, val):
        for i in xrange(i1, i2+1):
            self.array[i][j] = val

    def setHorizontal(self, i,j1,j2, val):
        for j in xrange(j1, j2+1):
            self.array[i][j] = val

    def setRectangle(self, i1,j1, i2,j2, val):
        for i in xrange(i1, i2+1):
            for j in xrange(j1, j2+1):
                self.array[i][j] = val

    def fillRegion(self, x,y, oldColour, newColour):
        # Recursive flood-fill algorithm

        if oldColour == newColour: return
        if self.array[x][y] != oldColour: return
        self.array[x][y] = newColour

        xabove = x-1
        if xabove < 0: xabove = 0

        xbelow = x+1
        if xbelow > self.rows-1: xbelow = self.rows-1

        yleft = y - 1
        if yleft < 0: yleft = 0

        yright = y + 1
        if yright > self.cols - 1: yright = self.cols - 1

        self.fillRegion(xabove, y, oldColour, newColour)
        self.fillRegion(xbelow, y, oldColour, newColour)
        self.fillRegion(x, yleft, oldColour, newColour)
        self.fillRegion(x, yright, oldColour, newColour)
        return

    def clear(self):
        for i in xrange(self.rows):
            for j in xrange(self.cols):
                self.array[i][j] = 0

    def show(self):
        for i in xrange(self.rows):
            for j in xrange(self.cols):
                print self.array[i][j],
            print

    def setName(self, name):
        self.name = name

if __name__ == '__main__':

    commands = [
        'I 5 6',
        'L 2 3 A',
        'S one.bmp',
        'G 2 3 J',
        'F 3 3 J',
        'V 2 3 4 W',
        'H 3 4 2 Z',
        'S two.bmp',
        'X'
    ]

    session = Session()
    for cmd in commands:
        session.processCommand(cmd)
