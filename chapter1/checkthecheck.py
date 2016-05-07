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
        rows = len(self.board)
        cols = len(self.board[0])
        for i in xrange(rows):
            for j in xrange(cols):
                print self.board[i][j],
            print

    def isWhite(self, piece):
        isWhite = True
        if piece.islower():
            isWhite = False
        return isWhite

    def isBlack(self, piece):
        return not self.isWhite(piece)

    def movePieces(self, turn):
        rows = len(self.board)
        cols = len(self.board[0])

        moveWhite = False
        if turn == 'white':
            moveWhite = True

        for i in xrange(rows):
            for j in xrange(cols):
                piece = self.board[i][j]

                if moveWhite:
                    if self.isBlack(piece):
                        continue

                else:  # Move black
                    if self.isWhite(piece):
                        continue

    # Taking moves
    def pawnTake(self, side):
        pass

    def knightTake(self, side):
        pass

    def bishopTake(self, side):
        pass

    def rookTake(self, side):
        pass

    def queenTake(self, side):
        pass

    def kingTake(self, side):
        pass

if __name__ == '__main__':
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

    chess = Chess(board)
    chess.show()
    chess.movePieces('white')