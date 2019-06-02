# -*- coding: utf-8 -*-
"""
Created on Thu May 30 12:16:10 2019

@author: awsir
"""
import matplotlib.pyplot as pp
import seaborn as sns
import os

def graph_color_gradient(arr, time_step, min_price, max_price, direct):
    """cmap = mp.colors.ListedColormap(['black', 'blue', 'red', 'white'])
    bounds=[-1, 25, 25, 50, 50, 75, 75, 101]
    norm = mp.colors.BoundaryNorm(bounds, cmap.N)
    img = pp.imshow(arr,interpolation='nearest',
                cmap = cmap,norm=norm)
    
    # make a color bar
    pp.colorbar(img,cmap=cmap,
            norm=norm,boundaries=bounds,ticks=[0, 25, 50, 75, 100])"""
    pp.rcParams['figure.figsize'] = 3,8
    ax = sns.heatmap(arr.grid[:, 1:-1, 0], xticklabels=False, yticklabels=False, vmin=0, vmax=1)
    newpath = os.path.join('D:', os.sep, "traffic_sims", str(direct), str("ETL_SIM_OUTPUT"), str(min_price), str(max_price))
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(newpath)
    pp.savefig(str(time_step) + '.png')
    pp.show()