import networkx as nx
import grid_graph

def swarm_algo(bot1_currentnode,bot1_target,bot2_currentnode,bot2_target,bot3_currentnode,bot3_target,bot4_currentnode,bot4_target):

    #Get next node from current node
    grid = grid_graph.grid_graph()
    bot1_path = nx.bidirectional_shortest_path(grid, bot1_currentnode, bot1_target)
    bot2_path = nx.bidirectional_shortest_path(grid, bot2_currentnode, bot2_target)
    bot3_path = nx.bidirectional_shortest_path(grid, bot3_currentnode, bot3_target)
    bot4_path = nx.bidirectional_shortest_path(grid, bot4_currentnode, bot4_target)
    if len(bot1_path) == 1:
        hold(bot1_path)
    if len(bot2_path) == 1:
        hold(bot2_path)
    if len(bot3_path) == 1:
        hold(bot3_path)
    if len(bot4_path) == 1:
        hold(bot4_path)

    ''' 1) Bots get into same nod '''
    if (bot1_path[1] == bot2_path[1]):
        print ("1 and 2 : Type 1")
        G = grid.copy()                     #Bot 2 will re-calculate the shortest path
        G.remove_node(bot1_path[1])         #By removing the busy node from the graph
        bot2_path = nx.bidirectional_shortest_path(G, bot2_currentnode, bot2_target)

    if (bot1_path[1] == bot3_path[1] ):
        print ("1 and 3 : Type 1")
        G = grid.copy()                     #Bot 3 will re-calculate the shortest path
        G.remove_node(bot1_path[1])         #By removing the busy node from the graph
        bot3_path = nx.bidirectional_shortest_path(G, bot3_currentnode, bot3_target)

    if (bot1_path[1] == bot4_path[1]):
        print ("1 and 4 : Type 1")
        G = grid.copy()                     #Bot 4 will re-calculate the shortest path
        G.remove_node(bot1_path[1])         #By removing the busy node from the graph
        bot4_path = nx.bidirectional_shortest_path(G, bot4_currentnode, bot4_target)

    if (bot2_path[1] == bot3_path[1]):
        print ("2 and 3 : Type 1")
        G = grid.copy()                     #Bot 3 will re-calculate the shortest path
        G.remove_node(bot2_path[1])         #By removing the busy node from the graph
        bot3_path = nx.bidirectional_shortest_path(G, bot3_currentnode, bot3_target)

    if (bot2_path[1] == bot4_path[1]):
        print ("2 and 4 : Type 1")
        G = grid.copy()                     #Bot 4 will re-calculate the shortest path
        G.remove_node(bot2_path[1])         #By removing the busy node from the graph
        bot4_path = nx.bidirectional_shortest_path(G, bot4_currentnode, bot4_target)

    if (bot3_path[1] == bot4_path[1]):
        print ("3 and 4 : Type 1")
        G = grid.copy()                     #Bot 4 will re-calculate the shortest path
        G.remove_node(bot3_path[1])         #By removing the busy node from the graph
        bot4_path = nx.bidirectional_shortest_path(G, bot4_currentnode, bot4_target)

    ''' 2) Bots cross head into each other '''
    if (bot1_path[0:2] == bot2_path[1::-1]):
        print ("1 and 2 : Type 2")
        G = grid.copy()                     #Bot 2 will re-calculate the shortest path
        G.remove_node(bot1_path[0])         #By removing the busy node from the graph
        bot2_path = nx.bidirectional_shortest_path(G, bot2_currentnode, bot2_target)

    if (bot1_path[0:2] == bot3_path[1::-1]):
        print ("1 and 3 : Type 2")
        G = grid.copy()                     #Bot 3 will re-calculate the shortest path
        G.remove_node(bot1_path[0])         #By removing the busy node from the graph
        bot3_path = nx.bidirectional_shortest_path(G, bot3_currentnode, bot3_target)

    if (bot1_path[0:2] == bot4_path[1::-1]):
        print ("1 and 4 : Type 2")
        G = grid.copy()                     #Bot 4 will re-calculate the shortest path
        G.remove_node(bot1_path[0])         #By removing the busy node from the graph
        bot4_path = nx.bidirectional_shortest_path(G, bot4_currentnode, bot4_target)

    if (bot2_path[0:2] == bot3_path[1::-1]):
        print ("2 and 3 : Type 2")
        G = grid.copy()                     #Bot 3 will re-calculate the shortest path
        G.remove_node(bot2_path[0])         #By removing the busy node from the graph
        bot3_path = nx.bidirectional_shortest_path(G, bot3_currentnode, bot3_target)

    if (bot2_path[0:2] == bot4_path[1::-1]):
        print ("2 and 4 : Type 2")
        G = grid.copy()                     #Bot 4 will re-calculate the shortest path
        G.remove_node(bot2_path[0])         #By removing the busy node from the graph
        bot4_path = nx.bidirectional_shortest_path(G, bot4_currentnode, bot4_target)

    if (bot3_path[0:2] == bot4_path[1::-1]):
        print ("3 and 4 : Type 2")
        G = grid.copy()                     #Bot 4 will re-calculate the shortest path
        G.remove_node(bot3_path[0])         #By removing the busy node from the graph
        bot4_path = nx.bidirectional_shortest_path(G, bot4_currentnode, bot4_target)

    print("\n")
    print("Bot 1 :" + str(bot1_path[0:2]))
    print("Bot 2 :" + str(bot2_path[0:2]))
    print("Bot 3 :" + str(bot3_path[0:2]))
    print("Bot 4 :" + str(bot4_path[0:2]))
    return (bot1_path[1],bot2_path[1],bot3_path[1],bot4_path[1])


#Holds the bot for some time when the destination reached
def hold(bot):
    bot.insert(0,bot[0])
    return bot

def reroute(bot):  #This needs to be modified

    return bot
