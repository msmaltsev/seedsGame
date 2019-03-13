#/usr/local/bin/python3
# -*- coding: utf-8 -*-

try:
    from os import getuid
except ImportError:
    def getuid():
        return 4000

from flask import Flask, render_template, request, redirect
from grid import *

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=['GET', 'POST'])
def index():

    g = Grid()
    nms = g.strt_nums
    g.addNums(g.add_nums_position, nms + [1,2,3,4])
    g.refreshGrid()
    
    result = []
    row = []
    for i in g.grid:
        row.append(i)
        if len(row) == g.width:
            result.append(row)
            row = []
    if row != []:
        result.append(row)
    
    grid_to_render = ''
    for row in result:
        tds_row = ''.join(['<td>%s</td>'%i for i in row])
        tr = '<tr>%s</tr>'%tds_row
        grid_to_render += '%s\n'%tr

    print(grid_to_render)

    return render_template('index.html', grid_to_render = grid_to_render)

if __name__ == '__main__':
    app.run(port=getuid() + 1000)
