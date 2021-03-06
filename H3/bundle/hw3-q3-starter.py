###############################################################################
# CS 224W (Fall 2019) - HW3
# Starter code for Problem 3
###############################################################################

import snap
import matplotlib.pyplot as plt

# Setup
num_voters = 10000
decision_period = 10


def read_graphs(path1, path2):
    """
    :param - path1: path to edge list file for graph 1
    :param - path2: path to edge list file for graph 2

    return type: snap.PUNGraph, snap.PUNGraph
    return: Graph 1, Graph 2
    """
    ###########################################################################
    # TODO: Your code here!
    Graph1 =snap.LoadEdgeList(snap.PUNGraph,path1,0,1)
    Graph2 =snap.LoadEdgeList(snap.PUNGraph,path2,0,1)
    ###########################################################################
    return Graph1, Graph2
#
#
def initial_voting_state(Graph):
    """
    Function to initialize the voting preferences.

    :param - Graph: snap.PUNGraph object representing an undirected graph

    return type: Python dictionary
    return: Dictionary mapping node IDs to initial voter preference
            ('A', 'B', or 'U')

    Note: 'U' denotes undecided voting preference.

    Example: Some random key-value pairs of the dict are
             {0 : 'A', 24 : 'B', 118 : 'U'}.
    """
    voter_prefs = {}
    ###########################################################################
    # TODO: Your code here!
    for Node in Graph.Nodes():
        NodeId =Node.GetId()
        LastDigit=  int( str(NodeId)[-1] )
        if LastDigit <=3:
            pref= 'A'
        elif  LastDigit <= 7:
            pref= 'B'
        else:
            pref = 'U'
        voter_prefs[NodeId] = pref
        
    ###########################################################################
    assert(len(voter_prefs) == num_voters)
    return voter_prefs
#


def iterate_voting(Graph, init_conf):
    """
    Function to perform the 10-day decision process.

    :param - Graph: snap.PUNGraph object representing an undirected graph
    :param - init_conf: Dictionary object containing the initial voting
                        preferences (before any iteration of the decision
                        process)

    return type: Python dictionary
    return: Dictionary containing the voting preferences (mapping node IDs to
            'A','B' or 'U') after the decision process.

    Hint: Use global variables num_voters and decision_period to iterate.
    """
    curr_conf = init_conf.copy()
    curr_alternating_vote = 'A'
    ###########################################################################
    # TODO: Your code here!
    undecided_NId = [ k   for k,v in  init_conf.items() if v  == 'U'  ]
    for i in range(decision_period):
        for NId in undecided_NId:
            Node=Graph.GetNI(NId)
            voter_dict ={'A':0,'B':0}
            for NbrNId in  Node.GetOutEdges():
                NbrPart=  curr_conf[NbrNId]
                if  NbrPart != 'U':
                    voter_dict[NbrPart] +=1

            if  voter_dict['A'] == voter_dict['B']:
                curr_conf[NId] = curr_alternating_vote
                curr_alternating_vote  = 'B' if  curr_alternating_vote=='A' else  'A'
            else:
                curr_conf[NId] = max(voter_dict,key=voter_dict.get ) 
    
    ###########################################################################
    return curr_conf



def sim_election(Graph):
    """
    Function to simulate the election process, takes the Graph as input and
    gives the final voting preferences (dictionary) as output.
    """
    init_conf = initial_voting_state(Graph)
    conf = iterate_voting(Graph, init_conf)
    return conf


from collections import Counter
def winner(conf):
    """
    Function to get the winner of election process.
    :param - conf: Dictionary object mapping node ids to the voting preferences

    return type: char, int
    return: Return candidate ('A','B') followed by the number of votes by which
            the candidate wins.
            If there is a tie, return 'U', 0
    """
    ###########################################################################
    # TODO: Your code here!
    counter=  Counter( conf.values() )
    if counter['A'] == counter['B']:
        return ('U',0)
    elif counter['A'] > counter['B']:
        return ('A',counter['A'] - counter['B'])
    else:
        return ('B',counter['B'] - counter['A'])
    ###########################################################################

def Q1():
    print ("\nQ1:")
    Gs = read_graphs('graph1.txt', 'graph2.txt')    # List of graphs

    # Simulate election process for both graphs to get final voting preference
    final_confs = [sim_election(G) for G in Gs]

    # Get the winner of the election, and the difference in votes for both
    # graphs
    res = [winner(conf) for conf in final_confs]
    
    for i in range(2):
        print ("In graph %d, candidate %s wins by %d votes" % (
                i+1, res[i][0], res[i][1]
        ))



#


import numpy as np
def Q2sim(Graph, k):
    """
    Function to simulate the effect of advertising.
    :param - Graph: snap.PUNGraph object representing an undirected graph
             k: amount to be spent on advertising

    return type: int
    return: The number of votes by which A wins (or loses), i.e. (number of
            votes of A - number of votes of B)

    Hint: Feel free to use initial_voting_state and iterate_voting functions.
    """
    ###########################################################################
    # TODO: Your code here!
    init_conf= initial_voting_state(Graph)
    start_NId =3000
    end_NId = int( np.floor(3000 + k/100 -1) )
    
    for NId in range(start_NId,end_NId+1):
        init_conf[NId]='A'
        
    conf= iterate_voting(Graph,init_conf)
    conf_couter = Counter(conf.values() )  
    return conf_couter['A'] - conf_couter['B']
    ###########################################################################

def find_min_k(diffs):
    """
    Function to return the minimum amount needed for A to win
    :param - diff: list of (k, diff), where diff is the value by which A wins
                   (or loses) i.e. (A-B), for that k.

    return type: int
    return: The minimum amount needed for A to win
    """
    ###########################################################################
    # TODO: Your code here!
    for k,diff in  diffs:
        if diff >0:
            return k 
    return  -1
    ###########################################################################


def makePlot(res, title):
    """
    Function to plot the amount spent and the number of votes the candidate
    wins by
    :param - res: The list of 2 sublists for 2 graphs. Each sublist is a list
                  of (k, diff) pair, where k is the amount spent, and diff is
                  the difference in votes (A-B).
             title: The title of the plot
    """
    Ks = [[k for k, diff in sub] for sub in res]
    res = [[diff for k, diff in sub] for sub in res]
    ###########################################################################
    # TODO: Your code here!
    for idx,(ks,diffs) in enumerate(zip(Ks,res) ):
        plt.plot(ks,diffs,label='Graph %d'%(idx+1))
    ###########################################################################
    plt.plot(Ks[0], [0.0] * len(Ks[0]), ':', color='black')
    plt.xlabel('Amount spent ($)')
    plt.ylabel('#votes for A - #votes for B')
    plt.title(title)
    plt.legend()
    plt.show()


def Q2():
    print ("\nQ2:")
    # List of graphs
    Gs = read_graphs('graph1.txt', 'graph2.txt')

    # List of amount of $ spent
    Ks = [x * 1000 for x in range(1, 10)]

    # List of (List of diff in votes (A-B)) for both graphs
    res = [[(k, Q2sim(G, k)) for k in Ks] for G in Gs]

    # List of minimum amount needed for both graphs
    min_k = [find_min_k(diff) for diff in res]

    formatString = "On graph {}, the minimum amount you can spend to win is {}"
    for i in range(2):
        print (formatString.format(i + 1, min_k[i]))

    makePlot(res, 'TV Advertising')


def Q3sim(Graph, k):
    """
    Function to simulate the effect of a dining event.
    :param - Graph: snap.PUNGraph object representing an undirected graph
             k: amount to be spent on the dining event

    return type: int
    return: The number of votes by which A wins (or loses), i.e. (number of
            votes of A - number of votes of B)

    Hint: Feel free to use initial_voting_state and iterate_voting functions.
    """
    ###########################################################################
    # TODO: Your code here!
    init_conf= initial_voting_state(Graph)
    NodeDegV = [  (v.GetVal1(),v.GetVal2())  for v in Graph.GetNodeInDegV() ]
    NodeDegV =sorted( NodeDegV,key=lambda item: (-item[1],item[0]) ,reverse=False)
    
    rollersNIds = [  NId  for NId,_  in   NodeDegV[: int(np.floor(k/1000))] ]
    for rollerNId in rollersNIds:
        init_conf[rollerNId] = 'A'
        
    conf = iterate_voting(Graph, init_conf)
    conf_couter = Counter(conf.values() )  
    return conf_couter['A'] - conf_couter['B']
    ###########################################################################


def Q3():
    print ("\nQ3:")
    # List of graphs
    Gs = read_graphs('graph1.txt', 'graph2.txt')

    # List of amount of $ spent
    Ks = [x * 1000 for x in range(1, 10)]

    # List of (List of diff in votes (A-B)) for both graphs
    res = [[(k, Q3sim(G, k)) for k in Ks] for G in Gs]

    # List of minimum amount needed for both graphs
    min_k = [find_min_k(diff) for diff in res]

    formatString = "On graph {}, the minimum amount you can spend to win is {}"
    for i in range(2):
        print (formatString.format(i + 1, min_k[i]))

    makePlot(res, 'Wining and Dining')


def getDataPointsToPlot(Graph):
    """
    :param - Graph: snap.PUNGraph object representing an undirected graph

    return values:
    X: list of degrees
    Y: list of frequencies: Y[i] = fraction of nodes with degree X[i]
    """
    ############################################################################
    # TODO: Your code here!
    X, Y = [], []
    total_nodes = Graph.GetNodes()
    for  pr in Graph.GetDegCnt():
        X.append(pr.GetVal1() )
        Y.append(pr.GetVal2()/ total_nodes)
    ############################################################################
    return X, Y


def Q4():
    """
    Function to plot the distributions of two given graphs on a log-log scale.
    """
    ###########################################################################
    # TODO: Your code here!
    print ("\nQ4:")
    # List of graphs
    Gs = read_graphs('graph1.txt', 'graph2.txt')
    
    x1, y1 = getDataPointsToPlot(Gs[0])
    x2, y2 = getDataPointsToPlot(Gs[1])
   
    plt.loglog(x1, y1, color = 'y', label = 'G1')     
    plt.loglog(x2, y2, linestyle = 'dashed', color = 'r', label = 'G2')
   
    plt.xlabel('Node Degree (log)')
    plt.ylabel('Proportion of Nodes with a Given Degree (log)')
    plt.title('Degree Distribution')
    plt.legend()
    plt.show()
    
    ###########################################################################


def main():
    Q1()
    Q2()
    Q3()
    Q4()


if __name__ == "__main__":
    main()
