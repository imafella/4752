from random import randint
from math import sqrt

# You shouldn't have to change this class, it just holds a sudoku board
# The board is represented internally by a 1D array, but you can call
# the get(row,col) function to index it via row, col
class Sudoku:
    
    def __init__(self, size):
        self.__board = [0]*(size*size)
        self.__size = size

    def set(self, row, col, val):   self.__board[self.get_index(row,col)] = val
    def randomize(self):            self.__board = [randint(1, self.size()) for i in range(len(self.__board))]
    def get_board(self):            return self.__board
    def get_index(self, row, col):  return self.size() * row + col
    def size(self):                 return self.__size
    def get(self, row, col):        return self.__board[self.get_index(row,col)]
    
    def row_count(self, row):
        count = [0]*(self.size()+1)
        for c in range(self.size()):
            count[self.get(row,c)] += 1
        return count

    def col_count(self, col):
        count = [0]*(self.size()+1)
        for r in range(self.size()):
            count[self.get(r,col)] += 1
        return count

    def square_count(self, sr, sc):
        sqsize = int(sqrt(self.size()))
        count = [0]*(self.size()+1)
        for r in range(sqsize):
            for c in range(sqsize):
                count[self.get(sr*sqsize+r, sc*sqsize+c)] += 1
        return count
    
    def set_arr(self, array):       
        self.__board = array
        self.__size = int(sqrt(len(array)))

    def print(self):
        for r in range(self.size()):
            for c in range(self.size()):
                print(self.get(r, c), end=' ')
            print('')
