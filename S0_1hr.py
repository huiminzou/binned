# -*- coding: utf-8 -*-
"""
Created on Tue May 29 11:12:11 2018
first, run segment.py to get individual files by drifter id
@author: huimin
"""


from datetime import datetime,timedelta
import numpy as np
from scipy import  interpolate
import pandas as pd
from SeaHorseTide import *

FList = np.genfromtxt('data/FList.csv',dtype=None,names=['FNs'],delimiter=',',skip_header=1)
FList1=[]
file_path='''data1/'''
time0=datetime(1858,11,17,00,00,00)
for a in np.arange(len(FList['FNs'])):
    times=[]
    hours=[]
    drifters = np.genfromtxt('''data/'''+FList['FNs'][a],dtype=None,names=['ids','time','lon','lat','depth'],delimiter=',',skip_header=1)  
    lon0=[]
    lat0=[]
    try:
        for b in np.arange(len(drifters['time'])):
            time=(datetime(int(drifters['time'][b][0:4]),int(drifters['time'][b][5:7]),int(drifters['time'][b][8:10]),int(drifters['time'][b][11:13]),int(drifters['time'][b][14:16]),int(drifters['time'][b][17:19])))
            hours.append((time-time0).days*24+(time-time0).seconds/3600.0)
            lon0.append(drifters['lon'][b])
            lat0.append(drifters['lat'][b])
    except:
        print 'next',a
    if hours!=[] and len(hours)>2:
        min_0=np.ceil(hours[0])
        max_0=np.floor(hours[-1])
        tdh=np.arange(min_0,max_0,1)
        try:
            lo=interpolate.interp1d(hours,lon0,kind='cubic')
            la=interpolate.interp1d(hours,lat0,kind='cubic')
            
            dr=dict(lon=[],lat=[],time=[])
            
            for c in np.arange(len(tdh)):
                dr['lon'].append(lo(tdh[c]).tolist())
                dr['lat'].append(la(tdh[c]).tolist())
                dr['time'].append(tdh[c])
        except:
            continue
        Coef=111111./86400.# deg/day -> m/s
        udh=[]
        vdh=[]
        lonz=[]
        latz=[]
        timez=[]
        tz=[]
        for i in range(1,len(dr['time'])-1):
            udh.append((dr['lon'][i+1]-dr['lon'][i-1])/((tdh[i+1]-tdh[i-1])/24.0)*Coef*np.cos(dr['lat'][i]*np.pi/180.))
            vdh.append((dr['lat'][i+1]-dr['lat'][i-1])/((tdh[i+1]-tdh[i-1])/24.0)*Coef)

            lonz.append(dr['lon'][i])
            latz.append(dr['lat'][i])
            timez.append(time0+timedelta(hours=tdh[i]))
            tz.append(tdh[i])
        # remove tidal signal
        udm=sh_rmtide(udh,ends=np.NaN)
        vdm=sh_rmtide(vdh,ends=np.NaN)
        print 'udm:',udm
        print 'vdm:',vdm
        udti=udh-udm
        vdti=vdh-vdm
        FN2='data1/'+FList['FNs'][a][:-4]+'.npz'
        FList1.append(FList['FNs'][a][:-4]+'.npz')
        np.savez(FN2,tz=tz,vdh=vdh,lonz=lonz,latz=latz,udh=udh,timez=timez,udti=udti,vdti=vdti,tdh=tdh,udm=udm,vdm=vdm)
dataframe = pd.DataFrame({'ids':FList1})#save as .csv format
dataframe.to_csv(file_path+"FList.csv",index=False,sep=',')