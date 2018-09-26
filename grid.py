#/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
from copy import deepcopy

class Grid():

    def __init__(self):

        strt_nums = [str(i) for i in range(1,20) if '0' not in str(i)]
        strt_nums = [int(i) for i in ''.join(list(strt_nums))]

        self.width = 9
        self.sep = ' '
        self.pointer = '>'
        self.grid = []
        self.pairlist = []
        self.available_pairs = False
        self.add_nums_position = (0,0) # (row, col)

        self.strt_nums = strt_nums


    def addNums(self, position, nums_row, verbose = False):

        if verbose:
            print('adding nums:', nums_row)

        if self.grid == []:
            self.grid = [[]]

        col = position[1]
        if col == 0 and self.grid != [[]]:
            self.grid.append([])

        grid_last_row = self.grid[-1]
        grid_last_row_cut = grid_last_row[:col]
        first_slice_len = self.width - len(grid_last_row_cut)
        first_slice, rest = nums_row[:first_slice_len], nums_row[first_slice_len:]

        new_grid_last_row_upd = grid_last_row_cut + first_slice

        if rest == []:

            add_nums_position_row = len(self.grid) - 1
            add_nums_position_col = len(new_grid_last_row_upd)

            if add_nums_position_col >= self.width:
                add_nums_position_row += 1
                add_nums_position_col = 0

            self.add_nums_position = (
                add_nums_position_row,
                add_nums_position_col
            )
            while len(new_grid_last_row_upd) < self.width:
                new_grid_last_row_upd.append(' ')
            
            self.grid[-1] = new_grid_last_row_upd

        else:
            
            self.grid[-1] = new_grid_last_row_upd
            rest_rows = []

            cnt = 0
            row = []
            while cnt < len(rest):
                row.append(rest[cnt])
                if len(row) == self.width:
                    rest_rows.append(row)
                    row = []
                cnt += 1
            if row != []:
                rest_rows.append(row)

            for row in rest_rows:
                self.grid.append(row)

            last_row = self.grid[-1]
            # print(last_row)

            add_nums_position_row = len(self.grid) - 1
            add_nums_position_col = len(last_row)

            # print('coord:', add_nums_position_row, add_nums_position_col)
                
            if add_nums_position_col >= self.width:
                add_nums_position_row += 1
                add_nums_position_col = 0

            self.add_nums_position = (
                add_nums_position_row,
                add_nums_position_col
            )

            while len(last_row) < self.width:
                last_row.append(self.sep)
            
    
    def nextNumsPosition(self):

        last_row = self.grid[-1]

        if last_row[-1] == self.sep:
            vertical_coord = len(self.grid) - 1
            horizontal_coord = len(last_row) - 1
            while last_row[-1] == self.sep:
                horizontal_coord -= 1
        else:
            horizontal_coord = 0
            vertical_coord = len(self.grid)

        return (horizontal_coord, vertical_coord)
    

    def substByCoordinate(self, x, y):
        x_arr = self.grid[x]
        x_arr[y] = self.sep
        self.grid[x] = x_arr
        return self.grid


    def isValidPair(self, a, b):
        if a == b or a + b == 10:
            return True
        else:
            return False


    def isPair(arr, index_a, index_b):
        btw = arr[index_a + 1:index_b]
        if btw == [] or list(set(btw)) == [self.sep]:
            return True
        else:
            return False


    def findHorizontalPairs(self): # pairs in rows
        
        # print('looking for HORIZONTAL pairs in grid:')
        # print(self.grid)

        pairs = []
        for arr_num in range(0, len(self.grid)):
            arr = self.grid[arr_num]

            while arr[-1] == self.sep:
                arr = arr[:-1]

            horizontal_coord = arr_num
            vertical_coord = 0
            while arr[vertical_coord] == self.sep:
                vertical_coord += 1
            while vertical_coord < len(arr) - 1:

                next_vertical_coord = vertical_coord + 1
                while arr[next_vertical_coord] == self.sep:
                    if next_vertical_coord < self.width - 1:
                        next_vertical_coord = next_vertical_coord + 1
                    else:
                        break

                fst_num = int(arr[vertical_coord])
                snd_num = int(arr[next_vertical_coord])

                if self.isValidPair(fst_num, snd_num):
                    pairs.append((
                        [horizontal_coord, vertical_coord], # first in pair
                        [horizontal_coord, next_vertical_coord] # second in pair
                    ))

                vertical_coord = next_vertical_coord
        return pairs


    def findVerticalPairs(self): # pairs in columns
        
        # print('looking for VERTICAL pairs in grid:')
        # print(self.grid)

        pairs = []
        for i in range(self.width):
            arr = [a[i] for a in self.grid]

            if list(set(arr)) == [self.sep]:
                continue
            else:

                while arr[-1] == self.sep:
                    arr = arr[:-1]

                vertical_coord = i
                horizontal_coord = 0

                while arr[horizontal_coord] == self.sep:
                    horizontal_coord += 1

                while horizontal_coord < len(arr) - 1:

                    next_horizontal_coord = horizontal_coord + 1
                    while arr[next_horizontal_coord] == self.sep:
                        if next_horizontal_coord < self.width:
                            next_horizontal_coord = next_horizontal_coord + 1
                        else:
                            break

                    fst_num = int(arr[horizontal_coord])
                    snd_num = int(arr[next_horizontal_coord])

                    if self.isValidPair(fst_num, snd_num):
                        pairs.append((
                            [horizontal_coord, vertical_coord],
                            [next_horizontal_coord, vertical_coord]
                            ))

                    horizontal_coord = next_horizontal_coord
        return pairs


    def findEdgePairs(self): # pairs on beginnings and ends of lines
        
        # print('looking for EDGE pairs in grid:')
        # print(self.grid)

        pairs = []

        rownum = 1

        while rownum != len(self.grid) - 1:

            a_last_index = -1
            while self.grid[rownum - 1][a_last_index] == self.sep:
                a_last_index -= 1
            a = int(self.grid[rownum - 1][a_last_index])
            a_coord = [rownum - 1, self.width + a_last_index]

            b_last_index = 0
            while self.grid[rownum][b_last_index] == self.sep:
                b_last_index += 1

            b = int(self.grid[rownum][b_last_index])
            b_coord = [rownum, b_last_index]

            if self.isValidPair(a, b):
                pairs.append((a_coord, b_coord))

            rownum += 1

        return pairs


    def getAllPairs(self):
        
        horizontal_pairs = self.findHorizontalPairs()
        vertical_pairs = self.findVerticalPairs()
        edge_pairs = self.findEdgePairs()
        all_pairs = horizontal_pairs + vertical_pairs + edge_pairs
        return all_pairs
    
    
    def getPairCoords(self):
        a_x = int(input('1st horiz: '))
        a_y = int(input('1st vertc: '))
        b_x = int(input('2nd horiz: '))
        b_y = int(input('2nd vertc: '))
        return ([a_x, a_y], [b_x, b_y])


    def comparePairs(self, user_pairs_arr):
        for p in self.pairlist:
            if p == user_pairs_arr:
                pass


    def refreshGrid(self, verbose = False):

        ap = self.getAllPairs()
        self.pairlist = ap
        if len(ap) == 0:
            self.available_pairs = False
        else:
            self.available_pairs = True

        if verbose:
            print('available_pairs: ', self.pairlist)
            print('add_nums_position: ', self.add_nums_position)


    def numsToAdd(self):
        grid_sum = [i for i in self.collectFromList(self.grid) if i != self.sep]
        return grid_sum


    def collectFromList(self, list_of_lists):
        ## берет на вход список списков
        ## возвращает сумму этих списков
        result = []
        for i in list_of_lists:
            if type(i) == list:
                result += self.collectFromList(i)
            else:
                result.append(i)
        return result


    def printGrid(self, verbose = False):

        if not verbose:
            os.system('clear')

        show_grid = deepcopy(self.grid)

        pointer_position = self.add_nums_position

        if verbose:
            print('GRID ROWS:', show_grid)
            print('POINTER POSITION: ', pointer_position)

        grid_length = len(show_grid)
        grid_length_digits = len(repr(grid_length))

        if len(show_grid) - 1 < pointer_position[0]:
            show_grid.append([self.pointer])
        else:
            rownum = pointer_position[1]
            colnum = pointer_position[0]
            show_grid[colnum][rownum] = self.pointer

        head = ' ' * grid_length_digits + '   ' + ' '.join([str(i) for i in range(0, self.width)])
        result = '%s\n\n'%head

        for arrnum in range (len(show_grid)):
            str_arrnum = str(arrnum)
            arr = [str(i) for i in show_grid[arrnum]]
            line_index = str_arrnum + ' ' * (grid_length_digits - len(str_arrnum)) + '   '
            line = line_index + ' '.join(arr)
            result += '%s\n'%line

        print('---------------------')
        print(result)
        print('---------------------')
    

if __name__ == '__main__':

    g = Grid()
    g.printGrid()
