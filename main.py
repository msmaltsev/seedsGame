#/usr/local/bin/python3
# -*- coding: utf-8 -*-

from grid import *


def main():

    g = Grid()
    g.addNums(g.add_nums_position, g.strt_nums)
    g.refreshGrid()
    g.printGrid(verbose=True)

    while True:

        while g.available_pairs:

            user_pair_coords = g.getPairCoords()
            if user_pair_coords in g.pairlist:
                for pair in user_pair_coords:
                    g.substByCoordinate(pair[0], pair[1])
            g.refreshGrid()
            g.printGrid(verbose=True)
            print(g.pairlist)
            print(g.grid)

        print('no more pairs available!')
        g.addNums(g.add_nums_position, g.numsToAdd())
        g.refreshGrid()
        g.printGrid()


if __name__ == '__main__':
    main()