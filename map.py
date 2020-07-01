import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import re
import datetime

def split_ddm(ddm):
    ddm = re.split('[°\s]+', ddm)
    if ddm[2] == 'N' or ddm[2] == 'E':
        return float(ddm[0]) + (float(ddm[1]) / 60)
    else:
        return -(float(ddm[0]) + (float(ddm[1]) / 60))

def to_dd_from_ddm(latitude, longitude):
    lat, lng = [], []
    for i in range(len(latitude)):
        lat.append(split_ddm(latitude[i]))
        lng.append(split_ddm(longitude[i]))
    return lat, lng

def draw_points(ax, xs, ys, text, clr):
    x, y = m(xs, ys)
    ax.scatter(x, y)
    for i, (cur_x, cur_y) in enumerate(zip(x, y)):
        ax.annotate(text[i], (cur_x, cur_y), color=clr)

fig, ax = plt.subplots(1, 1, figsize=(15,15))
m = Basemap(resolution='h',
            llcrnrlat=54, urcrnrlat=56,
            llcrnrlon=19, urcrnrlon=23, epsg=4326,
            ax=ax
            )
m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=1000, verbose=True)
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawstates(color='gray')

m.drawparallels(np.arange(50, 60, 0.5), labels=[1,1,1,1])
m.drawmeridians(np.arange(18, 24, 0.5), labels=[1,1,1,1])

#чтение и отрисовка городов
cities = pd.read_csv('cities.csv', sep=',')

cities_lat = cities['lat'].values
cities_lng = cities['lng'].values
cities_name = cities['city'].values

draw_points(ax, cities_lng, cities_lat, cities_name, 'aqua')

#чтение и отрисовка станций
stations = pd.read_csv('stations.csv', sep=',')

stations_lat, stations_lng = to_dd_from_ddm(stations['lat'].values, stations['lng'].values)
stations_num = stations['number'].values
draw_points(ax, stations_lng, stations_lat, stations_num, 'red')

plt.show()
