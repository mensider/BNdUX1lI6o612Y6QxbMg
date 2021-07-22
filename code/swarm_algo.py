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

    return (bot1_path[1],bot2_path[1],bot3_path[1],bot4_path[1])


#Holds the bot for some time, if there is a collision, or if the destination reached
def hold(bot):
    bot.append(bot[0])
    return bot
