# -*- coding: utf-8 -*-
"""
Created on Thu Jul 05 14:06:26 2018

@author: huimin
"""

import numpy as np
#from pydap.client import open_url
import matplotlib.pyplot as plt
from SeaHorseLib import *
from datetime import *
#from scipy import interpolate
import sys
from SeaHorseTide import *
import shutil
import matplotlib.mlab as mlab
import matplotlib.cm as cm

#HARDCODES
gridsize=0.05

def sh_bindata(x, y, z, xbins, ybins):
    """
    Bin irregularly spaced data on a rectangular grid.

    """
    ix=np.digitize(x,xbins)
    iy=np.digitize(y,ybins)
    xb=0.5*(xbins[:-1]+xbins[1:]) # bin x centers
    yb=0.5*(ybins[:-1]+ybins[1:]) # bin y centers
    zb_mean=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_median=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_std=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_num=np.zeros((len(xbins)-1,len(ybins)-1),dtype=int)    
    for iix in range(1,len(xbins)):
        for iiy in range(1,len(ybins)):
#            k=np.where((ix==iix) and (iy==iiy)) # wrong syntax
            k,=np.where((ix==iix) & (iy==iiy))
            zb_mean[iix-1,iiy-1]=np.mean(z[k])
            zb_median[iix-1,iiy-1]=np.median(z[k])
            zb_std[iix-1,iiy-1]=np.std(z[k])
            zb_num[iix-1,iiy-1]=len(z[k])
            
    return xb,yb,zb_mean,zb_median,zb_std,zb_num
#    return xb,yb,zb_median,zb_num

###########################################################

SOURCEDIR='data1/'

FList = np.genfromtxt(SOURCEDIR+'FList.csv',dtype=None,names=['FNs'],delimiter=',',skip_header=1)
FNs=list(FList['FNs'])

lath=np.array([])
lonh=np.array([])
th=np.array([])
#flagh=np.array([])
u=np.array([])
v=np.array([])
#for k in range(10):
for k in range(len(FNs)):
    FN=FNs[k]
    #ID_19965381.npz
    FN1=SOURCEDIR+FN
    print k, FN1
    Z=np.load(FN1)

    tdh=Z['tdh'];lonz=Z['lonz'];latz=Z['latz'];
    udh=Z['udh'];vdh=Z['vdh'];
    #tgap=Z['tgap'];flag=Z['flag'];
    udm=Z['udm'];vdm=Z['vdm'];
    #udti=Z['udti'];vdti=Z['vdti'];
    Z.close()
    
    lath=np.append(lath,latz)
    lonh=np.append(lonh,lonz)
    th=np.append(th,tdh)
    print 'th',th
    #flagh=np.append(flagh,flag)

    #u1=udh*flag
    #v1=vdh*flag
   # u=np.append(u,u1)            
   # v=np.append(v,v1)   
    u=np.append(u,udm)         
    v=np.append(v,vdm)

i=np.argwhere(np.isnan(u)==False).flatten()
u=u[i]
v=v[i]
lath=lath[i]
lonh=lonh[i]
th=th[i]

x=lonh
y=lath
  
xi = np.arange(-70.75,-70.00,gridsize)
yi = np.arange(41.63,42.12,gridsize)

xb,yb,ub_mean,ub_median,ub_std,ub_num = sh_bindata(x, y, u, xi, yi)
xb,yb,vb_mean,vb_median,vb_std,vb_num = sh_bindata(x, y, v, xi, yi)
np.savez('binned.npz',xb=xb,yb=yb,ub_mean=ub_mean,ub_median=ub_median,ub_std=ub_std,ub_num=ub_num,vb_mean=vb_mean,vb_median=vb_median,vb_std=vb_std,vb_num=vb_num)
