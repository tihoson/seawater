#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import plot
import data
import args

if __name__ == '__main__':
    args = args.parse_arg()

    data = data.Data(args.fname)

    lat, lng = 54.68, 19.7

    data.add_columns(data.calc_teos10_columns(lat, lng))

    data.save_to_file('out.csv')

    if args.show or args.save:
        plot.draw_plot(data.data, args.x_column, args.y_column, args.x_range, args.y_range, args.show, args.save)