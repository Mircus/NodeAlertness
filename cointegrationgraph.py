# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:10:19 2019

@author: mirco mannucci 
@author deborah koh tylor 
"""



import statsmodels.tsa.stattools as ts

import pandas as pd
from pandas_datareader import data as pdr

import time
import networkx as nx



import matplotlib.pyplot as plt 

tickers=[ 'VOD',  'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'AAPL', 'MS']
start = '2016-02-01'
end =   '2016-04-01'

s=time.time()
d = {}
for ticker in tickers:   
  try:
    d[ticker] = pdr.DataReader(ticker, "yahoo", start=start, end=end)
  except:
    print("An exception occurred downloading ticker " + ticker)
e=time.time()
print('downloaded ticker data in time: ' + str(e-s))

pan = pd.Panel(d)

df  = pan.minor_xs("Close")




   
res = {}
s=time.time()
for colx in df.columns.values:
    for coly in df.columns.values:
        if (colx != coly):
          try:
            res[colx, coly] = ts.coint(df[colx], df[coly])
          except:
            print("An exception occurred calculating coint for " + colx + " " + coly)
            
e=time.time()


print("results of cointegration in time: " + str(e-s))






lst_res=[]
for key in res:
    #make undirected edge list
    lst_res.append([key[0],key[1],res[key][1]])
df_coint = pd.DataFrame(lst_res)
df_coint.columns = ['source','target','weight_unnorm']
df_coint.head()


min_p = min(df_coint['weight_unnorm'].apply(lambda x: abs(x)))
max_p = max(df_coint['weight_unnorm'].apply(lambda x: abs(x)))

#flip so max cointegration (ie p=0) has a weight of 1
#weight range 0-1
df_coint['weight']=  df_coint['weight_unnorm'].apply(lambda x: 1.0 - ((abs(x)-min_p)/(max_p - min_p)))


df_coint['flooredweight']=  df_coint['weight'].apply(lambda x: x if (x >0.5) else 0)





tuples = [tuple(x) for x in df_coint[['source','target', 'flooredweight']].values]


# here goes some visualization of stocks cointegration graph 
# using the spring layout 

G = nx.MultiDiGraph()
G.add_weighted_edges_from(tuples)

print(tuples)

pos = nx.spring_layout(G, iterations= 500)
nx.draw_networkx_nodes(G, pos, node_color = 'r', node_size = 30, alpha = 1)

nx.draw_networkx_edges(G, pos)


labels = {}    
for node in G.nodes():
    
        #set the node name as the key and the label as its value 
  labels[node] = node
#Now only add labels to the nodes you require (the hubs in my case)
nx.draw_networkx_labels(G,pos,labels,font_size=16,font_color='b')
plt.show() 

