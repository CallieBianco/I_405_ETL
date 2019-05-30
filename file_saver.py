# -*- coding: utf-8 -*-
"""
Created on Thu May 30 12:16:10 2019

@author: awsir
"""
import matplotlib.pyplot as pp
import seaborn as sns

def graph_color_gradient(arr, time_step, min_price, max_price):
    """cmap = mp.colors.ListedColormap(['black', 'blue', 'red', 'white'])
    bounds=[-1, 25, 25, 50, 50, 75, 75, 101]
    norm = mp.colors.BoundaryNorm(bounds, cmap.N)
    img = pp.imshow(arr,interpolation='nearest',
                cmap = cmap,norm=norm)
    
    # make a color bar
    pp.colorbar(img,cmap=cmap,
            norm=norm,boundaries=bounds,ticks=[0, 25, 50, 75, 100])"""
    
    ax = sns.heatmap(arr.grid[:, :, 0], xticklabels=False, yticklabels=False, vmin=0, vmax=1)
    pp.savefig('./' + str("ETL_SIM_OUTPUT") + './' + str(min_price) + './' + str(max_price) + './' + str(time_step) + '-diffusion.png')
    pp.show()