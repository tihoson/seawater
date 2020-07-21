#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Draw and save a plot for the selected columns of dataframe
def draw_plot(data, x_column, y_column, x_range, y_range, show, save):
    if x_column == None or y_column == None:
        raise Exception('No axis selected')

    data.plot(x=x_column, y=y_column, xlim=x_range, ylim=y_range).set(xlabel=x_column, ylabel=y_column)
    if save:
        plt.savefig(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    if show:
        plt.show()
