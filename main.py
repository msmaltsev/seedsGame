#/usr/local/bin/python3
# -*- coding: utf-8 -*-

import argparse
from grid import *

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest='show_pairs', action='store_true', default=False, help='available pairs will be shown on each step')
args = parser.parse_args()

if __name__ == '__main__':
    
    g = Grid()
    g.show_pairs = args.show_pairs
    g.addNums(g.add_nums_position, g.strt_nums)
    g.refreshGrid()
    g.renderGrid()

    while True:

        while len(g.pairlist) > 0:

            if g.show_pairs:
                g.printPairlist()

            users_pair = g.getPairCoords()
            if users_pair in g.pairlist:
                for coord in users_pair:
                    g.substByCoordinate(coord)
                g.refreshGrid()
                g.renderGrid()
            else:
                g.refreshGrid()
                g.renderGrid(message = 'no such pair!')

        new_nums_row = g.getNewNumsRow()
        g.addNums(g.add_nums_position, new_nums_row)
        g.refreshGrid()
        g.renderGrid(message = 'no pairs left, new row added')




