#/usr/local/bin/python3
# -*- coding: utf-8 -*-

import argparse
from grid import *

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest='show_pairs', action='store_true', default=False, help='available pairs will be shown on each step')
args = parser.parse_args()

def main():

    log = open('log', 'w', encoding='utf8').close()

    g = Grid()
    g.show_pairs = args.show_pairs
    g.addNums(g.add_nums_position, g.strt_nums)
    g.refreshGrid()
    g.renderGrid()

    while True:

        if list(set(g.grid)) != [g.sep]:

            while len(g.pairlist) > 0:

                if g.show_pairs:
                    g.printPairlist()

                users_pair = g.getPairCoords()
                if users_pair[0] in g.pairlist:
                    log = open('log', 'a', encoding='utf8')
                    print('%s\t%s'%(users_pair[0], users_pair[1]), file=log)
                    log.close()
                    for coord in users_pair[0]:
                        g.substByCoordinate(coord)
                    g.refreshGrid()
                    g.renderGrid()
                else:
                    g.refreshGrid()
                    g.renderGrid(message = 'no such pair!')

            new_nums_row = g.getNewNumsRow()
            g.addNums(g.add_nums_position, new_nums_row)
            log = open('log', 'a', encoding='utf8')
            print('new nums row added', file=log)
            log.close()
            g.refreshGrid()
            g.renderGrid(message = 'no pairs left, new row added')

        else:

            print('congrats, you won!')
            print('stats are going to be printed out here')
            break


if __name__ == '__main__':
    main()
