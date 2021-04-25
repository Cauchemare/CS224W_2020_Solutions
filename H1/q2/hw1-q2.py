# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 18:07:21 2021

@author: luyao.li
"""

import snap
import numpy as np
import matplotlib.pyplot as plt


def GetLocalFeaturesSingleNode(Node,Graph):
    '''
    Params:
        Node :TUNGraphNI object,referred from 'for node in Graph.Nodes()'
        Graph : TUNGraph class
    Return:
        result: np.array( # nodes,3)
    '''
    deg=  Node.GetDeg()
    egonet,CntConEdges= Graph.GetEgonet(Node.GetId() )
    CntInEdges= egonet.GetEdges()
    return  np.array([deg,CntInEdges,CntConEdges],dtype=int)


def GetLocalFeature(Graph,n_feats=3):
    num_nodes=Graph.GetNodes()
    results = np.empty((num_nodes,n_feats),dtype= int)
    for  Node in  Graph.Nodes():
        NId= Node.GetId()
        result=  GetLocalFeaturesSingleNode(Node,Graph)
        results[NId,:] =result
        
    return results
def MostSimNIds(results,NId,topN=5):
    '''
    result: np.array(# nodes,# feats)
    NId: int,node index 
    topN:int ,most similar topN Nids 
    Return
     np.array( topN,) 返回最相近的Node ids
    '''
    results_norm2= np.linalg.norm(results,axis=1,keepdims= False)
    results_norm2 *= results_norm2[NId]
    
    multi_vecs= results @ results[NId,:]
    
    sim =[]
    for  otherNId,(m,n)    in enumerate( zip(multi_vecs,results_norm2)):
        if otherNId != NId:
            if n==0:
                elem= (otherNId,0.)
            else:
                elem= (otherNId, m/n)
            sim.append(elem)
    
    sim_sorted= sorted(sim,key= lambda item: item[1],reverse=True)
    if topN == -1:
        return sim_sorted
    else:
        return sim_sorted[:topN]


def Q1(filepath,nid=9,topN=5) :
    Graph= snap.TUNGraph.Load(snap.TFIn(filepath))
    LocalFeats = GetLocalFeature(Graph)
    mostSimNIds= MostSimNIds(LocalFeats,nid,topN)
    print(mostSimNIds)
    print(LocalFeats[nid])

def GetRecurFeature(Graph,K=2):
    localFeats= GetLocalFeature(Graph,3)
    for k in range(1,K+1):
        n_nodes,n_feats=  localFeats.shape 
        sumFeats= np.zeros_like(localFeats)
        meanFeats =np.zeros_like(localFeats,dtype=np.float32)
        for Node in  Graph.Nodes():
            DegSz = Node.GetDeg()
            NId= Node.GetId()
            if DegSz >0:
                sum_arr=  np.zeros((n_feats, ))
                for  ith in range(DegSz):
                    NbrNId =Node.GetNbrNId(ith)
                    sum_arr +=  localFeats[NbrNId]
                sumFeats[NId] = sum_arr
                meanFeats[NId] = sum_arr/DegSz
        localFeats= np.hstack( (localFeats,meanFeats,sumFeats))
    return localFeats

def Q2(filepath,nid=9,topN=5) :
    Graph= snap.TUNGraph.Load(snap.TFIn(filepath))
    recurFeats = GetRecurFeature(Graph)
    mostSimNIds= MostSimNIds(recurFeats,nid,topN)
    print(mostSimNIds)
    print(recurFeats[nid])
       
def Q3_a(filepath,NId=9,Nbins=20):
    #a
    Graph= snap.TUNGraph.Load(snap.TFIn(filepath))
    results = GetRecurFeature(Graph,2)
    mostSimNIds= MostSimNIds(results,NId,-1) 
    Sims= [item[1]  for item in mostSimNIds ] 
    
    
    plt.hist(Sims,bins= Nbins)
    plt.xlabel("cosine similarity with node %d"%NId)
    plt.ylabel("number of nodes(exclude %d node)"%NId )
    plt.show()
    
    return Graph, mostSimNIds

def GetSubGraph(Graph,NId,hops=3):
    NbrNIds = snap.TIntV()
    for hop in range(1,hops+1):
        _,NIdsAtHop= Graph.GetNodesAtHop(NId,hop,False)
        NbrNIds.extend(NIdsAtHop)
    NbrNIds.append(NId)  
    return Graph.GetSubGraph(NbrNIds)
        
from itertools import groupby
from operator import itemgetter
def Q3_b(filepath,NId=9,Nbins=20):
    
    Graph,mostSimNIds = Q3_a(filepath,NId=9,Nbins=20)
    sims= [item[1]  for item in mostSimNIds ]
    hist ,bin_edges= np.histogram( sims,bins=Nbins  )
    print(hist)
    print(bin_edges)
    select_bins = eval(input('select_bins:') )
    
    
    NIdBins =np.searchsorted(bin_edges,sims,side='right')
    filteredNIdBins=[ (simBins,NId)     for  NId,simBins in enumerate(NIdBins )  if simBins in select_bins]
    
    select_NId=[]
    for k,g in  groupby(filteredNIdBins,key= itemgetter(0)):
        filteredKNIds =[ item[1] for item in list(g)  ]
        RndNId= int(  np.random.choice( filteredKNIds,1)[0] )
        select_NId.append( (k,RndNId) )
    return Graph,select_NId
        

if  __name__ == '__main__':
#    Q1('hw1-q2.graph')
#    Q2('hw1-q2.graph')
    
    Graph,select_NId=Q3_b('hw1-q2.graph',9,20)
    NodesLabels={ Node.GetId(): str(Node.GetId()) for Node in Graph.Nodes() }
    
    for k, rnd_id in select_NId:
        SubGraph= GetSubGraph(Graph,rnd_id,hops=2)
        print('%d bins  subgraph'%k)
        SubGraph.DrawGViz(snap.gvlDot,'SubGraph_(%d,%d).png'%(k,rnd_id),"",NodesLabels)
    SubGraphEgo=GetSubGraph(Graph,9,hops=2)
    SubGraphEgo.DrawGViz(snap.gvlDot,'SubGraph_%d.png'%9,"",NodesLabels)
    