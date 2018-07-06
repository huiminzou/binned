# -*- coding: utf-8 -*-
"""
Created on Wed May 30 10:57:35 2018
seperate dataset to individual files by drifter ids, save as (.csv)
@author: huimin
"""
import csv
import numpy as np
import pandas as pd


#'drifters_cape_cod_bay.csv'     first ordered by id , then ordered by time
drifters = np.genfromtxt('drifters_cape_cod_bay.csv',dtype=None,names=['ids','time','lat','lon','depth','temp'],delimiter=',',skip_header=1)

n=[]
n.append(0)
for a in np.arange(len(drifters['ids'])-1):
    if drifters['ids'][a]!=drifters['ids'][a+1]:
        n.append(a+1)
n.append(len(drifters['ids']))
#f='julu.csv'
FList=[]
file_path='''data/'''
#csvfile1 = file(f, 'wb')
for a in np.arange(len(n)-1):
    drift=dict(ids=[],time=[],lon=[],lat=[],depth=[])
    for b in np.arange(len(drifters['ids'])):
        if b>=n[a] and b<n[a+1]:
            print b
            drift['ids'].append(drifters['ids'][b])
            drift['time'].append(drifters['time'][b])
            drift['depth'].append(-abs(drifters['depth'][b]))
            drift['lon'].append(drifters['lon'][b])
            drift['lat'].append(drifters['lat'][b])
    drifter_data=[]
    drifter_data.append(drift['ids'])
    drifter_data.append(drift['time'])
    drifter_data.append(drift['lon'])
    drifter_data.append(drift['lat'])
    drifter_data.append(drift['depth'])
    
    dr=map(list, zip(*drifter_data))
    FN2=file_path+str(drifters['ids'][n[a]])+'.csv'
    #writer1 = csv.writer(csvfile1)
    #writer1.writerows([str(a)+'.csv'])
    csvfile = file(FN2, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['ids', 'time', 'lon','lat','depth'])
    writer.writerows(dr)
    csvfile.close()
    FList.append(str(drifters['ids'][n[a]])+'.csv')
#csvfile1.close()
dataframe = pd.DataFrame({'ids':FList})#save as .csv format
dataframe.to_csv(file_path+"FList.csv",index=False,sep=',')
