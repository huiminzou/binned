# -*- coding: utf-8 -*-
"""
Created on Thu Jul 05 15:01:58 2018
Program to plot the bin-averaged velocities & standard deviations using the "arrow" command.
It imports the "binned.npz" file created by previous program.
@author: huimin in July 2018
contributions from JiM mostly in the form of comments and documentation

NOTE: this assumes you have run a series of programs:
-ERDDAP download of drifters data
-segment.py to make individual drifter files
-s0_1hr.py to get hourly data and remove tide
-s1_mean.py to bin
"""

import numpy as np
import matplotlib.pyplot as plt
import netCDF4
###################HARDCODE########################
# do you actually use this function?
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
# www.ngdc.noaa.gov
# world vector shoreline ascii
FNCL='necscoast_worldvec.dat'
# lon lat pairs
# segments separated by nans

CL=np.genfromtxt(FNCL,names=['lon','lat'])

FN='binned.npz'
#FN='binned_model.npz'
Z=np.load(FN) 
xb=Z['xb']
yb=Z['yb']
ub_mean=Z['ub_mean']
ub_median=Z['ub_median']
ub_std=Z['ub_std']
ub_num=Z['ub_num']
vb_mean=Z['vb_mean']
vb_median=Z['vb_median']
vb_std=Z['vb_std']
vb_num=Z['vb_num']
Z.close()
# what is the purpose of this for-loop that follows?
# If there are less than "10" observations, you set to "nan" because you don't think that is enough to define a good velocity?
for a in np.arange(len(ub_num)):
    for b in np.arange(len(ub_num[0])):
        if ub_num[a][b]<10:
            ub_num[a][b]=0
            ub_mean[a][b]=np.nan
            vb_mean[a][b]=np.nan
duf=ub_mean
dvf=vb_mean
aa=np.empty((len(ub_mean),len(ub_mean[0])),dtype=ub_mean.dtype)
for a in np.arange(len(ub_mean)):
    for b in np.arange(len(ub_mean[0])):
        aa[a,b]=np.sqrt(ub_mean[a,b]*ub_mean[a,b]+vb_mean[a,b]*vb_mean[a,b])
        
dv=aa

xxb,yyb = np.meshgrid(xb, yb)
cc=np.arange(-1.5,1.500001,0.05) # what is "cc"

plt.figure()
ub = np.ma.array(ub_mean, mask=np.isnan(ub_mean))
vb = np.ma.array(vb_mean, mask=np.isnan(vb_mean))
for a in np.arange(len(ub_mean)):
    for b in np.arange(len(ub_mean[0])):
        if ub_mean[a][b]==np.nan:
            ub_mean[a][b]=0
        if vb_mean[a][b]==np.nan:
            vb_mean[a][b]=0

for a in np.arange(len(xxb)):
    for b in np.arange(len(xxb[0])):
        plt.arrow(xxb[a][b],yyb[a][b],ub_mean.T[a][b]/8,vb_mean.T[a][b]/8,head_width=.01)# why divide by "8"?
plt.arrow(-70.1,41.7,0.05,0,head_width=.01)# again, you do not want these numbers in the middle of the code.
plt.text(-70.1,41.72,'$5cm/s$')        

plt.title(FN[:-4]+', mean')
plt.plot(CL['lon'],CL['lat'])
plt.axis([-70.75,-70,41.63,42.12])
plt.savefig('binned_drifter_mean')
plt.show()

plt.figure()
ub = np.ma.array(ub_std, mask=np.isnan(ub_mean))
vb = np.ma.array(vb_std, mask=np.isnan(vb_mean))

for a in np.arange(len(ub_std)):
    for b in np.arange(len(ub_std[0])):
        if ub_std[a][b]==np.nan:
            ub_std[a][b]=0
        if vb_std[a][b]==np.nan:
            vb_std[a][b]=0

for a in np.arange(len(xxb)):
    for b in np.arange(len(xxb[0])):
        plt.arrow(xxb[a][b],yyb[a][b],ub_std.T[a][b]/10,vb_std.T[a][b]/10,head_width=.01)
plt.arrow(-70.1,41.7,0.05,0,head_width=.01)# if you divide the data by 10, you need to divide the legend by 10
plt.text(-70.1,41.72,'$5cm/s$')         

plt.title(FN[:-4]+', std')

plt.plot(CL['lon'],CL['lat'])
plt.axis([-70.75,-70,41.63,42.12])
plt.savefig('binned_drifter_std')
plt.show()

ubn = np.ma.array(ub_num, mask=np.isnan(ub_num))
vbn = np.ma.array(vb_num, mask=np.isnan(vb_num))
plt.figure()

for a in np.arange(len(xxb[0])):
    for b in np.arange(len(yyb)):
        if -70.75<xxb[0][a]<-70 and 41.63<yyb[b][0]<42.12:
            plt.text(xxb[0][a],yyb[b][0],ub_num[a][b])
plt.plot(CL['lon'],CL['lat'])
plt.axis([-70.75,-70,41.63,42.12])
plt.title('binned_drifter_num')
plt.savefig('binned_drifter_num')
plt.show()
  
plt.figure()
plt.title('sea_depth')
   
data = np.genfromtxt('sea.csv',dtype=None,names=['x','y','h'],delimiter=',')    
x=[]
y=[]
h=[]
x=data['x']
y=data['y']
h=data['h']
xi = np.arange(-70.75,-70.00,0.03)
yi = np.arange(41.63,42.12,0.03)
xb,yb,hb_mean,hb_median,hb_std,hb_num = sh_bindata(x, y, h, xi, yi)
xxxb,yyyb = np.meshgrid(xb, yb)
CS=plt.contour(xxxb, yyyb, -abs(hb_mean.T))
plt.clabel(CS, inline=1, fontsize=10)
plt.plot(CL['lon'],CL['lat'])
plt.axis([-70.75,-70,41.63,42.12])
plt.savefig('sea_depth')   
plt.show()
