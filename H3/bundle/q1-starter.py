import snap
import numpy as np
import matplotlib.pyplot as plt

def load_graph(name):
    '''
    Helper function to load graphs.
    Use "epinions" for Epinions graph and "email" for Email graph.
    Check that the respective .txt files are in the same folder as this script;
    if not, change the paths below as required.
    '''
    if name == "epinions":
        G = snap.LoadEdgeList(snap.PNGraph, "soc-Epinions1.txt", 0, 1)
    elif name == 'email':
        G = snap.LoadEdgeList(snap.PNGraph, "email-EuAll.txt", 0, 1)   
    else: 
        raise ValueError("Invalid graph: please use 'email' or 'epinions'.")
    return G

def q1_1():
    '''
    You will have to run the inward and outward BFS trees for the 
    respective nodes and reason about whether they are in SCC, IN or OUT.
    You may find the SNAP function GetBfsTree() to be useful here.
    '''
    
    ##########################################################################
    #TODO: Run outward and inward BFS trees from node 2018, compare sizes 
    #and comment on where node 2018 lies.
    G = load_graph("email")
    #Your code here:
    
    def q1_1_sub(G,StartNId):
        
        outBfs= G.GetBfsTree(StartNId,True,False)
        inBfs = G.GetBfsTree(StartNId,False,True)
        return outBfs.GetNodes(),inBfs.GetNodes()  
       
    email_result = q1_1_sub( G,2018)
    print(G.GetMxSccSz())
    print('total:{0},outgoing:{1},incoming:{2}'.format(G.GetNodes(),email_result[0],email_result[1]  ))
    
    
    ##########################################################################
    
    ##########################################################################
    #TODO: Run outward and inward BFS trees from node 224, compare sizes 
    #and comment on where node 224 lies.
    G = load_graph("epinions")
    #Your code here:
    epinions_result=  q1_1_sub( G,224)
    print('total:{0},outgoing:{1},incoming:{2}'.format(G.GetNodes(),epinions_result[0],epinions_result[1]  ))
    print(G.GetMxSccSz())
    ##########################################################################

    print ('2.1: Done!\n')


def q1_2():
    '''
    For each graph, get 100 random nodes and find the number of nodes in their
    inward and outward BFS trees starting from each node. Plot the cumulative
    number of nodes reached in the BFS runs, similar to the graph shown in 
    Broder et al. (see Figure in handout). You will need to have 4 figures,
    one each for the inward and outward BFS for each of email and epinions.
    
    Note: You may find the SNAP function GetRndNId() useful to get random
    node IDs (for initializing BFS).
    '''
    ##########################################################################
    #TODO: See above.
    #Your code here:
    def q1_2_sub(G,NumIds):
        rnd=  snap.TRnd()
        rnd.Randomize()
        outNodesCnt= []
        inNodesCnt =[]
        for i in range (NumIds):
            RndNId = G.GetRndNId(rnd)
            BfsOutTree =G.GetBfsTree(RndNId,True,False)
            outNodesCnt.append(BfsOutTree.GetNodes() )  
            BfsInTree =G.GetBfsTree(RndNId,False,True)
            inNodesCnt.append( BfsInTree.GetNodes()  )
        return  sorted(outNodesCnt), sorted(inNodesCnt)
    def  q1_2_plot(GType):
        x= np.linspace(0,1,100,endpoint=False)
        G = load_graph(GType)
        print('total',G.GetNodes())
        outNodesCnt,inNodesCnt =q1_2_sub(G,100)
        fig,(ax1,ax2)= plt.subplots(1,2)
        fig.suptitle(GType)
        ax1.set_title('out')
        ax1.plot(x,outNodesCnt)
        ax2.set_title('in')
        ax2.plot(x, inNodesCnt)
        
    q1_2_plot('email')
    q1_2_plot('epinions')        
    
    ##########################################################################
    print ('2.2: Done!\n')

def q1_3():
    '''
    For each graph, determine the size of the following regions:
        DISCONNECTED
        IN
        OUT
        SCC
        TENDRILS + TUBES
        
    You can use SNAP functions GetMxWcc() and GetMxScc() to get the sizes of 
    the largest WCC and SCC on each graph. 
    '''
    ##########################################################################
    #TODO: See above.
    #Your code here:
    def q1_3_sub(GType):
        
        
        G = load_graph(GType)
        MxScc = G.GetMxScc()
        MxWcc= G.GetMxWcc()
        num_disconnected= G.GetNodes() - MxWcc.GetNodes()
        num_scc= MxScc.GetNodes()  
        BfsTree_in = G.GetBfsTree(20,False,True)
        BfsTree_out = G.GetBfsTree(20,True,False)
        num_in = BfsTree_in.GetNodes()-  num_scc
        num_out=  BfsTree_out.GetNodes()-  num_scc
        num_tubes=  G.GetNodes()  - num_scc-num_in -num_out -num_disconnected
        print('DISCONNECTED {0},IN {1},OUT {2},SCC {3},TENDRILS+ TUBES :{4}'
              .format( num_disconnected,num_in,num_out,num_scc, num_tubes  )    )
        
    q1_3_sub('email')
    q1_3_sub('epinions')
    

    
    
    ##########################################################################
    print ('2.3: Done!\n' )

def q1_4():
    '''
    For each graph, calculate the probability that a path exists between
    two nodes chosen uniformly from the overall graph.
    You can do this by choosing a large number of pairs of random nodes
    and calculating the fraction of these pairs which are connected.
    The following SNAP functions may be of help: GetRndNId(), GetShortPath()
    '''
    ##########################################################################
    #TODO: See above.
    #Your code here:
    def q1_4_sub(GType,num_iters= 10000):
        rnd_start =snap.TRnd()
        rnd_end = snap.TRnd()
        rnd_start.Randomize()
        rnd_end.Randomize()
        
        G = load_graph(GType)
        num_connected = 0
        for i in  range(num_iters):
            SrcNId=  G.GetRndNId(rnd_start) 
            DestNId= G.GetRndNId(rnd_end)
            if G.GetShortPath(SrcNId,DestNId,True) != -1:
                num_connected +=1
        print('connected fraction :{0:.4f}'.format(  num_connected/ num_iters  )     )
    q1_4_sub('email')   
    q1_4_sub('epinions')    
    
    ##########################################################################
    print ('2.4: Done!\n')
    
if __name__ == "__main__":
#    q1_1()
#    q1_2()  
#    q1_3()
    '''
    DISCONNECTED 40382,IN 151023,OUT 17900,SCC 34203,TENDRILS+ TUBES :21706
    DISCONNECTED 2,IN 24236,OUT 15453,SCC 32223,TENDRILS+ TUBES :3965
    '''
    q1_4()
#    print ("Done with Question 2!\n")