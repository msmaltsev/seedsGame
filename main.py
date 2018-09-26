#/usr/local/bin/python3
# -*- coding: utf-8 -*-

from grid import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest='show_pairs', action='store_true', default=False, help='available pairs will be shown on each step')
parser.add_argument('-r', '--rules', dest='show_rules', action='store_true', default=False, help='show rules and quit')
args = parser.parse_args()


def main():

    g = Grid()
    g.addNums(g.add_nums_position, g.strt_nums)
    g.refreshGrid()
    g.printGrid()
    if args.show_pairs:
        print('AVAILABLE PAIRS:', g.pairlist)

    while True:

        while g.available_pairs:

            user_pair_coords = g.getPairCoords()
            if user_pair_coords in g.pairlist:
                for pair in user_pair_coords:
                    g.substByCoordinate(pair[0], pair[1])
            g.refreshGrid()
            g.printGrid()
            if args.show_pairs:
                print('AVAILABLE PAIRS:', g.pairlist)

        print('no more pairs available!')
        g.addNums(g.add_nums_position, g.numsToAdd())
        g.refreshGrid()
        g.printGrid()


if __name__ == '__main__':

    if args.show_rules:
        
        f = open('rules.txt', 'r', encoding='utf8').read()
        print(f)

    else:
        main()