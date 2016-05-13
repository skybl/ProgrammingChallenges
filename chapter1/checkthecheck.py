from math import fabs

def isFreeSquare(nm):
    if nm == '.':
        return True
    else:
        return False

def getPieceValue(name):
    nm = name.lower()
    if nm == 'k':
        value = 6
    elif nm == 'q':
        value = 5
    elif nm == 'b':
        value = 4
    elif nm == 'n':
        value = 3
    elif nm == 'r':
        value = 2
    elif nm == 'p':
        value = 1
    else:
        value = 0
    return value

class Piece:
    def __init__(self, name, x,y, board):
        self.name = name
        self.x = x
        self.y = y
        self.colour = 'black'
        if self.isWhite():
            self.colour = 'white'
        self.value = getPieceValue(name)
        self.possibleMoves = self.getPossibleMoves(board)

    def isWhite(self, nm=None):
        isWhite = True
        if nm == None:
            if self.name.islower():
                isWhite = False
        else:
            if nm.islower():
                isWhite = False
        return isWhite

    def isBlack(self, nm=None):
        if nm == None:
            return not self.isWhite()
        else:
            return not self.isWhite(nm)

    def showPieceMoves(self):
        # Make board
        board = []
        for i in xrange(8):
            row = []
            for j in xrange(8):
                row.append('.')
            board.append(row)

        piece = self
        moves = self.possibleMoves

        board[piece.x][piece.y] = piece.name
        for i, j in moves:
            board[i][j] = '*'

        for i in xrange(8):
            for j in xrange(8):
                print board[i][j],
            print
        print

    def getPossibleMoves(self, board):
        # Determines all possible moves for a single piece on board
        # These moves need to be checked again outside this function
        # by checking for obstructions between current and new position
        # NB: Neglects castling and moves into check
        moves = []

        if self.name in ('p', 'P'):  # Cannot move backwards
            if self.name == 'p':  # Moves down board
                moves.append((self.x + 1, self.y))
                moves.append((self.x + 1, self.y - 1))
                moves.append((self.x + 1, self.y + 1))
                if self.isBlack() and self.x == 1:  # Jump two squares at start
                    moves.append((self.x + 2, self.y))
            else:  # Moves up board
                moves.append((self.x - 1, self.y))
                moves.append((self.x - 1, self.y - 1))
                moves.append((self.x - 1, self.y + 1))
                if self.isWhite() and self.x == 6:
                    moves.append((self.x - 2, self.y))
        else:
            nm = self.name.lower()
            if nm == 'k':
                moves.append((self.x - 1, self.y))  # Up
                moves.append((self.x + 1, self.y))  # Down
                moves.append((self.x, self.y - 1))  # Left
                moves.append((self.x, self.y + 1))  # Right

                moves.append((self.x - 1, self.y - 1))  # Up left
                moves.append((self.x - 1, self.y + 1))  # Up right
                moves.append((self.x + 1, self.y - 1))  # Down left
                moves.append((self.x + 1, self.y + 1))  # Down right
            elif nm == 'q':
                moves.extend(self.getCrossMoves())
                moves.extend(self.getDiagonalMoves())
            elif nm == 'b':
                moves.extend(self.getDiagonalMoves())
            elif nm == 'n':
                moves.append((self.x - 1, self.y - 2))  # Up left left
                moves.append((self.x - 1, self.y + 2))  # Up right right

                moves.append((self.x + 1, self.y - 2))  # Down left left
                moves.append((self.x + 1, self.y + 2))  # Down right right

                moves.append((self.x - 2, self.y - 1))  # Up up left
                moves.append((self.x - 2, self.y + 1))  # Up up right

                moves.append((self.x + 2, self.y - 1))  # Down down left
                moves.append((self.x + 2, self.y + 1))  # Down down right
            elif nm == 'r':
                moves.extend(self.getCrossMoves())

        filteredMoves = []
        for move in moves:  # Filter off moves outside boundaries
            x, y = move
            if 0 <= x < 8 and 0 <= y < 8 and not (x == self.x and y == self.y):
                filteredMoves.append(move)

        # return filteredMoves
        return self.filterLegalMoves(filteredMoves, board)

    def filterLegalMoves(self, moves, board):
        filteredMoves = []

        whitesTurn = False
        if self.isWhite():
            whitesTurn = True

        for move in moves:
            endi, endj = move
            endSquare = board[endi][endj]
            lowerName = self.name.lower()

            # Check that end square is empty or has opponent piece
            if not isFreeSquare(endSquare):
                if (whitesTurn and self.isWhite(endSquare)) or \
                        (not whitesTurn and self.isBlack(endSquare)):
                    continue

            if lowerName == 'k':  # Local mover
                filteredMoves.append(move)

            elif lowerName == 'p':  # Long range movers
                if self.y == endj:  # Move in same column
                    if not isFreeSquare(endSquare):  # Cannot take piece
                        continue
                    elif fabs(self.x - endi) == 2.0:  # Cannot jump over piece
                        if (self.isWhite() and not isFreeSquare(board[self.x - 1][self.y])) or \
                                (self.isBlack() and not isFreeSquare(board[self.x + 1][self.y])):
                            continue
                filteredMoves.append(move)

            elif lowerName in ('q', 'b', 'r'):  # Long range movers
                transMoves = []
                transMoves.extend(self.getTransitionMoves(endi, endj))

                # Check that all transition moves do not obstruct path to end square
                isLegalMove = True
                for transMove in transMoves:
                    transi, transj = transMove
                    if transi == endi and transj == endj:
                        break
                    if not isFreeSquare(board[transi][transj]):
                        isLegalMove = False
                        break
                # End-for

                if isLegalMove:
                    filteredMoves.append(move)

            elif lowerName == 'n':  # Knight can hop over pieces
                pass

            else:
                raise Exception('Invalid piece %s' % (self.name))

        return filteredMoves

    def getCrossMoves(self):
        moves = []

        for i in xrange(self.x - 1, -1, -1):  # Up
            moves.append((i, self.y))
        for i in xrange(self.x + 1, 8):  # Down
            moves.append((i, self.y))

        for j in xrange(self.y - 1, -1, -1):  # Left
            moves.append((self.x, j))
        for j in xrange(self.y + 1, 8):  # Right
            moves.append((self.x, j))

        return moves

    def getDiagonalMoves(self):
        moves = []

        j = self.y + 1
        for i in xrange(self.x - 1, -1, -1):  # Up right
            if j == 8:
                break
            moves.append((i, j))
            j += 1

        j = self.y - 1
        for i in xrange(self.x - 1, -1, -1):  # Up left
            if j == -1:
                break
            moves.append((i, j))
            j -= 1

        j = self.y + 1
        for i in xrange(self.x + 1, 8):  # Down right
            if j == 8:
                break
            moves.append((i, j))
            j += 1

        j = self.y - 1
        for i in xrange(self.x + 1, 8):  # Down left
            if j == -1:
                break
            moves.append((i, j))
            j -= 1

        return moves

    def getTransitionMoves(self, endx, endy):
        transMoves = []

        # Determine directions
        incx = 0
        if endx < self.x:  # Upwards
            incx = -1
        elif endx > self.x:  # Downwards
            incx = 1

        incy = 0
        if endy < self.y:  # Left
            incy = -1
        elif endy > self.y:  # Right
            incy = 1

        # NB: Either or both incx and incy are nonzero

        # Go towards end position
        if incx == 0:
            for j in xrange(self.y + incy, endy, incy):
                transMoves.append((self.x, j))
        else:
            j = self.y + incy
            for i in xrange(self.x + incx, endx, incx):
                if incy != 0 and j == endy:
                    break
                transMoves.append((i, j))
                j += incy

        return transMoves

class Move:
    def __init__(self, piece, x,y):
        self.piece = piece
        self.x = x
        self.y = y

class Chess:
    def __init__(self, board):
        self.board = []
        for line in board:
            row = []
            for c in line:
                row.append(c)
            self.board.append(row)
        rows = len(self.board)
        cols = len(self.board[0])
        if rows != 8 and cols != 8:
            raise Exception('Invalid board dimensions %d %d'%(rows, cols))

    def show(self):
        for i in xrange(8):
            for j in xrange(8):
                print self.board[i][j],
            print
        print

    def getMovablePieces(self, turn):
        allMovablePieces = []  # Find all pieces for side that could move in this turn

        moveWhite = False
        if turn == 'white':
            moveWhite = True

        for i in xrange(8):
            for j in xrange(8):
                place = self.board[i][j]
                if place != '.':
                    piece = Piece(place, i,j, self.board)
                    if (moveWhite and piece.isBlack()) or \
                            (not moveWhite and piece.isWhite()):
                        continue
                    else:
                        if len(piece.possibleMoves) > 0:
                            allMovablePieces.append(piece)

                        #if piece.name == 'b':
                        #    piece.showPieceMoves()
        # End for

        return allMovablePieces

    def evaluateMoves(self, turn):
        bestMoveValue = None

        if turn not in ('white', 'black'):
            raise Exception('Invalid side %s'%(turn))

        allMovablePieces = self.getMovablePieces(turn)
        bestMoveValue = 0

        if len(allMovablePieces) > 0:
            allMovesAcrossPieces = []
            for piece in allMovablePieces:
                bestMove = self.getMostValuableMove(piece.possibleMoves)  # NB: Could be empty
                allMovesAcrossPieces.append(bestMove)

            bestMove = self.getMostValuableMove(allMovesAcrossPieces)
            endi, endj = bestMove
            if self.board[endi][endj] == 'k':
                print 'black king is in check.'
            elif self.board[endi][endj] == 'K':
                print 'white king is in check.'

            bestMoveValue = getPieceValue(self.board[endi][endj])

        return bestMoveValue

    def getMostValuableMove(self, moves):
        # In the absence of any AI, make most valuable move
        scores = [0] * len(moves)
        for index, move in enumerate(moves):
            endi, endj = move
            if not isFreeSquare(self.board[endi][endj]):
                pieceToTake = Piece(self.board[endi][endj], endi, endj, self.board)
                scores[index] = pieceToTake.value
        bestPieceMoveIndex = scores.index(max(scores))
        return moves[bestPieceMoveIndex]

if __name__ == '__main__':
    boards = []
    board = [
        '..k.....',
        'ppp.pppp',
        '........',
        '.R...B..',
        '........',
        '........',
        'PPPPPPPP',
        'K.......'
    ]
    boards.append(board)

    board = [
        'rnbqk.nr',
        'ppp..ppp',
        '....p...',
        '...p....',
        '.bPP....',
        '.....N..',
        'PP..PPPP',
        'RNBQKB.R'
    ]
    boards.append(board)

    board = [
        '........',
        '........',
        '........',
        '........',
        '........',
        '........',
        '........',
        '........'
    ]
    boards.append(board)

    kingTakeValue = getPieceValue('k')

    for index,board in enumerate(boards):
        chess = Chess(board)
        #chess.show()
        print 'Game #', index+1, ':',
        v1 = chess.evaluateMoves('white')
        v2 = chess.evaluateMoves('black')
        if kingTakeValue not in (v1, v2):
            print 'no king is in check.'
