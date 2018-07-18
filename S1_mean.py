# -*- coding: utf-8 -*-
"""
Created on Thu Jul 05 14:06:26 2018
Program to bin U&V velocities as derived from drifter obs as stored in the "data1" directory
and outputs a "binned.npz" file in the "data1" directory
@author: Huimin borrowing some code from Xiajian and Vitalii
contributions from JiM in July 2018 in the form of documentation

NOTE: The following programs are typically run prior to this:
- ERDDAP download of drifter obs
- segment.py to get individual drifter files
- S0_1hr.py to get hourly data AND remove tide
"""

import numpy as np
import matplotlib.pyplot as plt
from SeaHorseLib import *
from datetime import *
import sys
from SeaHorseTide import *
import shutil
import matplotlib.mlab as mlab
import matplotlib.cm as cm

#HARDCODES#################
gridsize=0.05                    # is this in units of degrees?
gbox=[-70.75,-70.00,41.63,42.12] # geographic box of interest w/lon_west,lon_east,lat_south,lat_north
###########################

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
            k,=np.where((ix==iix) & (iy==iiy)) # I have never seen this ",=" syntax before
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
    udh=Z['udh'];vdh=Z['vdh']; # hourly u & v
    #tgap=Z['tgap'];flag=Z['flag'];
    udm=Z['udm'];vdm=Z['vdm']; # what is this?  It is not model is it? 
    #udti=Z['udti'];vdti=Z['vdti'];
    Z.close()
    
    lath=np.append(lath,latz)# what are you doing here? What is "lath" vs "latz"
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
# this geographic box needs to be defined at the top of the code.  
xi = np.arange(gbox[1],gbox[2],gridsize) # creates a string of longitudes
yi = np.arange(gbox[3],gbox[4],gridsize) # creates a string of latitudes

xb,yb,ub_mean,ub_median,ub_std,ub_num = sh_bindata(x, y, u, xi, yi)
xb,yb,vb_mean,vb_median,vb_std,vb_num = sh_bindata(x, y, v, xi, yi)
np.savez('binned.npz',xb=xb,yb=yb,ub_mean=ub_mean,ub_median=ub_median,ub_std=ub_std,ub_num=ub_num,vb_mean=vb_mean,vb_median=vb_median,vb_std=vb_std,vb_num=vb_num)
