#/usr/local/bin/python3
# -*- coding: utf-8 -*-

# 1) находит инвалидные пары
# 2) разворачивать пару, введённу. пользователем
# 3) очистка экрана после каждого хода

from grid import *
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest='show_pairs', action='store_true', default=False, help='available pairs will be shown on each step')
parser.add_argument('-r', '--rules', dest='show_rules', action='store_true', default=False, help='show rules and quit')
parser.add_argument('-v', dest='verbose', action = 'store_true', default=False, help='print info')
args = parser.parse_args()


def main():

    verbose = args.verbose

    g = Grid()
    g.addNums(g.add_nums_position, g.strt_nums)
    if verbose:
        print('REFRESHING GRID')
    g.refreshGrid()
    if verbose:
        print('PRINTING REFRESHED GRID')
    g.printGrid(verbose)
    if args.show_pairs:
        print('AVAILABLE PAIRS:', g.pairlist)
    if verbose:
        print(g.grid)


    while True:

        while g.available_pairs:

            user_pair_coords = g.getPairCoords()
            user_pair_coords_inverse = (user_pair_coords[1], user_pair_coords[0])
            for pair in [user_pair_coords, user_pair_coords_inverse]:
                if pair in g.pairlist:
                    for coords in user_pair_coords:
                        g.substByCoordinate(coords[0], coords[1])
                    break
            if verbose:
                print('REFRESHING GRID')
            g.refreshGrid()
            if verbose:
                print('PRINTING REFRESHED GRID')
            g.printGrid(verbose)
            if args.show_pairs:
                print('AVAILABLE PAIRS:', g.pairlist)
            if verbose:
                print(g.grid)

        print('no more pairs available!')
        g.addNums(g.add_nums_position, g.numsToAdd())
        if verbose:
            print('REFRESHING GRID')
        g.refreshGrid()
        if verbose:
            print('PRINTING REFRESHED GRID')
        g.printGrid(verbose)
        if args.show_pairs:
            print('AVAILABLE PAIRS:', g.pairlist)
        if verbose:
            print(g.grid)

if __name__ == '__main__':

    if args.show_rules:

        f = open('rules.txt', 'r', encoding='utf8').read()
        print(f)

    else:
        main()