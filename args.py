import argparse

# For arg parser
def rang(s):
    x, y = map(int, s.split(','))
    return x, y

# Command line parser
def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-file', action='store', dest='fname', help='input file')
    parser.add_argument('-x', action='store', dest='x_column', help='column for x axis')
    parser.add_argument('-y', action='store', dest='y_column', help='column for y axis')
    parser.add_argument('-xrange', action='store', dest='x_range', default=None, type=rang, help='range in format start,end for x axis')
    parser.add_argument('-yrange', action='store', dest='y_range', default=None, type=rang, help='range in format start,end for y axis')
    parser.add_argument('-show', action='store_true', help='show graph of a function')
    parser.add_argument('-save', action='store_true', help='save as png')

    args = parser.parse_args()

    if args.fname == None:
        raise Exception('No file selected')

    return args