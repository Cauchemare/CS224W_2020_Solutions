# -*- coding: utf-8 -*-

"""
CS 224W(2019 Fall) - HW0
@author: luyao.li
"""
'''
1
'''
import snap
G =snap.TNGraph.New()
G.AddNode(1)
G.AddNode(2)
G.AddNode(3)
G.AddEdge(1,2)
G.AddEdge(2,1)
G.AddEdge(1,3)
G.AddEdge(1,1) 

print(G.GetNodes())
print(G.CntSelfEdges())
print(G.CntUniqDirEdges())
print(G.CntUniqUndirEdges())
print(G.CntUniqBiDirEdges())
print(G.CntOutDegNodes(0)  )
print(G.CntInDegNodes(0) )

print(len([(item.GetVal1(),item.GetVal2()) for  item in G.GetNodeOutDegV()  if item.GetVal2()  > 10]) )
print(len([(item.GetVal1(),item.GetVal2()) for  item in G.GetNodeInDegV()  if item.GetVal2()  < 10]) )


'''
2
'''
import numpy as np

#2.1
G= snap.LoadEdgeList(snap.PNGraph,'Wiki-Vote.txt',0,1)
import matplotlib.pyplot as plt 
items = G.GetOutDegCnt()
x=[ item.GetVal1()   for item in items if item.GetVal1() !=0]
y=[ item.GetVal2()   for item in items if item.GetVal1() !=0]

plt.figure(figsize=(15,10))
plt.title('N of nodes vs out-degree',fontsize= 'xx-large')
plt.xlabel('out-degree(log)',fontsize= 'xx-large')
plt.ylabel('number of nodes(log)',fontsize ='xx-large')
plt.xlim(xmin= np.min(x) ,xmax= np.max(x)  )
plt.loglog(x,y)

#2.2
slope,intercept =np.polyfit(np.log10(x),np.log10(y),deg=1)
abline=  slope* np.log10(x) +intercept
plt.loglog(x,np.power(10,abline),'--')
plt.show()

'''
3
'''
#3.1
G= snap.LoadEdgeList(snap.PNGraph,'stackoverflow-Java.txt',0,1)
print(G.GetWccs().Len())  #10143
MxWcc= G.GetMxWcc()
print(    MxWcc.GetEdges() ,MxWcc.GetNodes())  #322486 131188
#3.2
pagerank= G.GetPageRank()
pagerank.SortByDat(False)
print( pagerank.keys()[:3] )  #[992484, 135152, 22656]
#3.3
NIdHubH,NIdAutH = G.GetHits() 
NIdHubH.SortByDat(False)
NIdAutH.SortByDat(False)
print(NIdHubH.keys()[:3],NIdAutH.keys()[:3] )  #[892029, 1194415, 359862] [22656, 157882, 571407]











