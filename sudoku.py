#!/usr/bin/python3 -B
import math, sys, time, os, getopt
class Sudoku:
    def __init__(self, speed):
        self.iteration_n    = 0
        self.speed          = speed / 1000

    def print_there(self, x, y, text):
        sys.stdout.write('\x1b7\x1b[%d;%df%s\x1b8' % (x, y, text))
        sys.stdout.flush()
    
    def get_show_text(self, block):
        text    = ''
        for row in range(9):
            if row % 3 == 0:
                text    += '+' + '-'*23 + '+\n'
            for col in range(9):
                if col % 3 == 0:
                    text    += '| '
                text    += str(block[row][col]) + ' '
                if col == 8:
                    text    += '|\n'
            if row == 8:
                text    += '+' + '-'*23 + '+'
        return text
    
    def get_pval(self, block, row, col):
        # get possible values
        row_s   = math.floor(row / 3) * 3
        col_s   = math.floor(col / 3) * 3
        dval    = block[row] # by row
        dval    = dval + [d[col] for d in block] # by col
        dval    = dval + block[row_s][col_s:col_s+3] + block[row_s+1][col_s:col_s+3] + block[row_s+2][col_s:col_s+3] # by 3x3
        pval    = list(set([1,2,3,4,5,6,7,8,9]) - set(dval))
        pval.sort()
        return pval
    
    def get_next(self, block):
        for r in range(9):
            for c in range(9):
                if block[r][c] == 0:
                    return r, c
                elif r == 8 and c == 8:
                    return -1, -1
    
    def resolve(self, block):
        row, col    = self.get_next(block)
        if row == -1 and col == -1: #Done
            return block
        else:
            pval    = self.get_pval(block, row, col)
            self.print_there(15, 10, str(self.iteration_n))
            self.print_there(16, 0, self.get_show_text(block))
            self.iteration_n   += 1
            time.sleep(self.speed)
            while len(pval) != 0:
                block[row][col] = pval.pop(0)
                block_next  = self.resolve(block)
                if block_next is not False:
                    return block_next
            if len(pval) == 0:
                block[row][col] = 0
                return False
    def do(self, din):
        os.system('clear')
        print('Input:')
        print(self.get_show_text(din))
        
        print('Process:')
        dout    = self.resolve(din)
        print('\n'*12)

        print('Output:')
        print(self.get_show_text(dout))


# Main
fname       = 'default.txt'
speed       = 0
opts, args  = getopt.getopt(sys.argv[1:], 'i:s:')
for op, val in opts:
    if op == '-i':
        fname   = val
    elif op == '-s':
        speed   = val

din     = [[0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
with open(fname, 'r') as fp:
    din_str = fp.readlines()
    for row in range(9):
        for col in range(9):
            din[row][col]   = int(din_str[row][col])
sudoku  = Sudoku(speed)
sudoku.do(din)
