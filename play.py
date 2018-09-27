#/usr/local/bin/python3
# -*- coding: utf-8 -*-

import argparse, time, re, random, sys
from grid import *

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest='show_pairs', action='store_true', default=False, help='available pairs will be shown on each step')
parser.add_argument('-a', dest='auto', action='store_true', default=False, help='autoplay')
parser.add_argument('-r', dest='repl', action='store_true', default=False, help='replay')
args = parser.parse_args()

def main(auto = args.auto):

    if auto:
        log = open('autoplay_log', 'w', encoding='utf8').close()
    else:
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

                if auto:
                    users_pair = (random.choice(g.pairlist), None)
                else:
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

                if auto:
                    time.sleep(0.5)

            if auto:
                time.sleep(0.5)

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


def replay(logfile = 'log'):

    try:
        log = open(logfile, 'r', encoding='utf8')
    except:
        print('no log provided, can not run')
        sys.exit()


    g = Grid()
    g.show_pairs = args.show_pairs
    g.addNums(g.add_nums_position, g.strt_nums)
    g.refreshGrid()
    g.renderGrid()
    time.sleep(0.5)

    for line in log:
        print(line)
        m = re.search('\(([0-9]+), ([0-9]+)\)', line)
        if m is not None:
            pair = (int(m.group(1)), int(m.group(2)))
            for coord in pair:
                g.substByCoordinate(coord)
            g.refreshGrid()
            g.renderGrid()
            time.sleep(0.5)
        else:
            m = re.search('new nums row', line)
            if m is not None:
                new_nums_row = g.getNewNumsRow()
                g.addNums(g.add_nums_position, new_nums_row)
                g.refreshGrid()
                g.renderGrid()

if __name__ == '__main__':
    if args.repl:
        replay()
    else:
        main()
