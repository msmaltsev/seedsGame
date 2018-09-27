#/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os, platform
from copy import deepcopy

class Grid():

    def __init__(self):

        strt_nums = [str(i) for i in range(1,20) if '0' not in str(i)]
        strt_nums = [int(i) for i in ''.join(list(strt_nums))]

        self.width = 9
        self.sep = ' '
        self.pointer = '>'
        self.pointer_position = 0
        self.grid = []
        self.pairlist = []
        self.available_pairs = False
        self.add_nums_position = 0
        self.strt_nums = strt_nums
        self.show_pairs = False


    def getNewNumsRow(self):
        new_nums = [i for i in self.grid if i != self.sep]
        return new_nums


    def addNums(self, add_nums_position, new_nums_row):
        self.grid = self.grid[:add_nums_position]
        self.grid += new_nums_row
        self.add_nums_position = len(self.grid)


    def getNumIndex(self, x, y):
        return self.width * x + y

    
    def getPairCoords(self):

        print('FIRST ROW THEN COL')

        a_x = self.validatedInput('1st x: ', 'bad type. 1st_x: ')
        a_y = self.validatedInput('1st y: ', 'bad type. 1st y: ')
        b_x = self.validatedInput('2nd x: ', 'bad type. 2nd x: ')
        b_y = self.validatedInput('2nd y: ', 'bad type. 2nd y: ')
        
        a_num_index = self.getNumIndex(a_x, a_y)
        b_num_index = self.getNumIndex(b_x, b_y)

        pair = (a_num_index, b_num_index)

        return pair


    def validatedInput(self, caption, mistake_caption, allowed_type = 'int', max_attempts = 0):
        if max_attempts == 0:
            max_attempts = 1000000
        attempts = 0
        type_is_right = False
        value = input(caption)
        while not type_is_right:
            if attempts < max_attempts:
                try:
                    value = eval('%s("%s")'%(allowed_type, value))
                    type_is_right = True
                    break
                except Exception as e:
                    attempts += 1
                    value = input(mistake_caption)
            else:
                print('too much attempts. killing program')
                sys.exit()

        return value


    def isValidPair(self, a, b):
        a, b = int(a), int(b)
        if a == b or a + b == 10:
            return True
        else:
            return False


    def substByCoordinate(self, coord):
        self.grid[coord] = self.sep


    def findXPairs(self):

        search_grid = deepcopy(self.grid)
        while search_grid[-1] == self.sep:
            search_grid = search_grid[:-1]

        pairs = []

        index = 0
        while index < len(search_grid) - 1:
            fst_index = index
            fst_value = search_grid[fst_index]
            if fst_value == self.sep:
                try:
                    index += 1
                    continue
                except:
                    break
            # print('fst_index: %s'%fst_index)
            # print('fst_value: %s'%fst_value)
            snd_index = fst_index + 1
            snd_value = search_grid[snd_index]
            while snd_value == self.sep:
                try:
                    snd_index += 1
                    snd_value = search_grid[snd_index]
                except: break
            # print('snd_index: %s'%snd_index)
            # print('snd_value: %s'%snd_value)
            # print(fst_value, snd_value)
            if self.isValidPair(fst_value, snd_value):
                pairs.append((fst_index, snd_index))

            index = snd_index

        return pairs


    def findYPairs(self):

        pairs = []

        turned_grid = []
        for i in range(self.width):
            col = [(self.grid[k], k) for k in range(len(self.grid)) if k % self.width == i]
            turned_grid += col

        turned_grid = [k for k in turned_grid if k[0] != self.sep]

        index = 0
        while index < len(turned_grid) - 1:
            fst_index = index
            fst_tuple = turned_grid[fst_index]
            fst_value = fst_tuple[0]

            if fst_value == self.sep:
                index += 1
                continue

            snd_index = fst_index + 1
            snd_tuple = turned_grid[snd_index]
            snd_value = snd_tuple[0]

            while snd_value == self.sep:
                snd_index += 1
                snd_tuple = turned_grid[snd_index]
                snd_value = snd_tuple[0]

            if self.isValidPair(fst_value, snd_value):
                fst_i = fst_tuple[1]
                snd_i = snd_tuple[1]
                if fst_i < snd_i:
                    pairs.append((fst_i, snd_i))

            index = snd_index

        return pairs


    def refreshGrid(self):

        while len(self.grid) % self.width != 0:
            self.grid.append(self.sep)
        
        x_pairs = self.findXPairs()
        y_pairs = self.findYPairs()
        pairs = x_pairs + y_pairs
        reverse_pairs = [(i[1], i[0]) for i in pairs]
        pairs += reverse_pairs
        self.pairlist = pairs


    def computeCoordinates(self, coord):
        return (int(coord / self.width), coord % self.width)


    def printPairlist(self):

        result = []

        for p in self.pairlist:
            first = self.computeCoordinates(p[0])
            second = self.computeCoordinates(p[1])

            result.append((first, second))

        print(result)

    
    def renderGrid(self, message = ''):

        if platform.version() == 'Windows':
            os.system('cls')
        else:
            os.system('clear') 

        result = ''

        grid_to_show = deepcopy(self.grid)
        try:
            grid_to_show[self.add_nums_position] = self.pointer
        except:
            grid_to_show.append(self.pointer)

        arr_to_show = []
        row = []
        for i in grid_to_show:
            row.append(i)
            if len(row) == self.width:
                arr_to_show.append(row)
                row = []
        if row != []:
            arr_to_show.append(row)

        horiz_coords = range(self.width - 1)
        vertc_coords = range(len(arr_to_show) - 1)
        vertc_space_length = len(repr(len(grid_to_show)))
        
        for rownum in range(len(arr_to_show)):
            str_rownum = str(rownum)
            arr = [str(i) for i in arr_to_show[rownum]]
            line_index = str_rownum + ' ' * (vertc_space_length - len(str_rownum)) + '   '
            line = line_index + ' '.join(arr)
            result += '%s\n'%line

        head = ' ' + ' ' * (vertc_space_length - len(str_rownum)) + '   ' + ' '.join([str(i) for i in range(0, self.width)])
        result = '%s\n\n%s'%(head, result)

        print('------------------------')
        print(result)
        print('------------------------')
        print(message)


if __name__ == '__main__':

    pass
