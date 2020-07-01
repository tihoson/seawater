import pandas as pd
import matplotlib.pyplot as plt
import datetime
import argparse
import gsw

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

    return args

if args.fname == None:
    raise Exception('No file selected')

if args.x_column == None or args.y_column == None:
    raise Exception('No axis selected')

def read(fname): 
    data = pd.read_csv(fname, sep='\s+', parse_dates=['Date', 'Time'])
    for column in data.columns:
        if column != 'Date' and column != 'Time':
           data[column].astype(float)
           

    return data

def prepare_data(data):
    data = data.drop([i for i in range(data['Pres'].idxmax() + 1, len(data))])
    data = data.sort_values(by=['Pres'])

    i, cur = 1, 0
    while i < len(data):
        if data.iloc[cur].name > data.iloc[i].name:
            data = data.drop(data.iloc[i].name)
        else:
            cur += 1
            i = cur + 1

    return data

def draw_plot(data, x_column, y_column, x_range, y_range, show, save):
    data.plot(x=x_column, y=y_column, xlim=x_range, ylim=y_range).set(xlabel=x_column, ylabel=y_column)
    if save:
        plt.savefig(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    if show:
        plt.show()

def rang(s):
    x, y = map(int, s.split(','))
    return x, y


data = read(args.fname)
data = prepare_data(data)

print(gsw.SA_from_SP(data['Sal'].values, data['Pres'].values, 19, 54))

draw_plot(data, args.x_column, args.y_column, args.x_range, args.y_range, args.show, args.save)