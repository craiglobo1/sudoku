import copy
import random

class SudokuBoard:
    def __init__(self,rows=9,columns=9):
        self.rows = rows
        self.columns = columns
    def makeBoard(self):
        # self.board = self.construct_puzzle_solution()
        # self.board = self.pluck()
        self.board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def construct_puzzle_solution(self):
    # Loop until we're able to fill all 81 cells with numbers, while
    # satisfying the constraints above.
        while True:
            try:
                puzzle  = [[0]*9 for i in range(9)] # start with blank puzzle
                rows    = [set(range(1,10)) for i in range(9)] # set of available
                columns = [set(range(1,10)) for i in range(9)] #   numbers for each
                squares = [set(range(1,10)) for i in range(9)] #   row, column and square
                for i in range(9):
                    for j in range(9):
                        # pick a number for cell (i,j) from the set of remaining available numbers
                        choices = rows[i].intersection(columns[j]).intersection(squares[(i//3)*3 + j//3])
                        choice  = random.choice(list(choices))
            
                        puzzle[i][j] = choice
            
                        rows[i].discard(choice)
                        columns[j].discard(choice)
                        squares[(i//3)*3 + j//3].discard(choice)

                # success! every cell is filled.
                return puzzle
            
            except IndexError:
                # if there is an IndexError, we have worked ourselves in a corner (we just start over)
                pass
    
    def pluck(self,n=0):
            puzzle = self.board
            """
            Answers the question: can the cell (i,j) in the puzzle "puz" contain the number
            in cell "c"? """
            def canBeA(puz, i, j, c):
                v = puz[c//9][int(c%9)]
                if puz[i][j] == v: return True
                if puz[i][j] in range(1,10): return False
                    
                for m in range(9): # test row, col, square
                    # if not the cell itself, and the mth cell of the group contains the value v, then "no"
                    if not (m==c//9 and j==c%9) and puz[m][j] == v: return False
                    if not (i==c//9 and m==c%9) and puz[i][m] == v: return False
                    if not ((i//3)*3 + m//3==c//9 and (j//3)*3 + int(m%3) == int(c%9) ) and puz[(i//3)*3 + m//3][(j//3)*3 + int(m%3)] == v:
                        return False

                return True


            """
            starts with a set of all 81 cells, and tries to remove one (randomly) at a time
            but not before checking that the cell can still be deduced from the remaining cells. """
            cells     = set(range(81))
            cellsleft = cells.copy()
            while len(cells) > n and len(cellsleft):
                cell = random.choice(list(cellsleft)) # choose a cell from ones we haven't tried
                cellsleft.discard(cell) # record that we are trying this cell

                # row, col and square record whether another cell in those groups could also take
                # on the value we are trying to pluck. (If another cell can, then we can't use the
                # group to deduce this value.) If all three groups are True, then we cannot pluck
                # this cell and must try another one.
                row = col = square = False

                for i in range(9):
                    if i != cell//9:
                        if canBeA(puzzle, i, int(cell%9), cell): row = True
                    if i != cell%9:
                        if canBeA(puzzle, cell//9, i, cell): col = True
                    if not (((cell/9)/3)*3 + i/3 == cell/9 and ((cell//9)%3)*3 + i%3 == cell%9):
                        if canBeA(puzzle, ((cell//9)//3)*3 + i//3, ((cell//9)%3)*3 + i%3, cell): square = True

                if row and col and square:
                    continue # could not pluck this cell, try again.
                else:
                    # this is a pluckable cell!
                    puzzle[cell//9][cell%9] = 0 # 0 denotes a blank cell
                    cells.discard(cell) # remove from the set of visible cells (pluck it)
                    # we don't need to reset "cellsleft" because if a cell was not pluckable
                    # earlier, then it will still not be pluckable now (with less information
                    # on the board).

            # This is the puzzle we found, in all its glory.
            return puzzle


    def printBoard(self):
        if not self.board:
            print('Error: Board is not made')
        else:
            for row in range(len(self.board)):
                if row % 3 == 0 and row != 0:
                    print("- - - - - - - - - - - - - -")
                for column in range(len(self.board)):
                    if column % 3 == 0 and column != 0:
                        print('|',end='')
                    
                    print(f' {self.board[row][column]} ',end='')

                    if column == 8:
                        print()
    
    def valid(self,num,pos):
        x,y = pos

        for i in range(len(self.board)):

            if self.board[x][i] == num and i != y:  # checking for repeated no in row
                return False
            
            if self.board[i][y] == num and i != x:  # checking for repeated no in coloumn
                return False

        boxX = x // 3
        boxY = y // 3

        for row in range(boxX*3,boxX*3):
            for column in range(boxY*3,boxY*3):
                if self.board[row][column] == num and pos != (row,column):
                    return False

        return True

    def findEmpty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)  # row, col
        return None

    
    def solve(self):
        find = self.findEmpty()
        if not find:
            return True
        else:
            row,col = find
        for i in range(1,10):
            if self.valid(i,(row,col)):
                self.board[row][col] = i
            
                if self.solve():
                    return True

                self.board[row][col] = 0
        return False    



    def action(self,num,pos):
      row,col = pos
      self.board[row][column] = num



