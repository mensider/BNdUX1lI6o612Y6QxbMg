# The Plan
# --------
# [.] Use an image of the arean as background
# [.] Define 4 rect blocks, each for a bot
# [.] Assume a precursor fn which will provide coordinates of each bot
# [.] Go Plan Epsilon

import turtle
import swarm_algo
import time
import grid_graph
import node_translator

#Setup the Arena
arena=turtle.Screen()
arena.bgpic(picname="Arena.png")
arena.setup(width=1000,height=480)
'''
arena_origin_y = 215.5
arena_origin_x = -72.5
arena_blocksize = 47.5
'''
#Define bot objects
bot1 = turtle.Turtle()
bot2 = turtle.Turtle()
bot3 = turtle.Turtle()
bot4 = turtle.Turtle()
#Define bot colors
bot1.color("pink")
bot2.color("green")
bot3.color("red")
bot4.color("blue")
#Define bot shapes
bot1.shape("square")
bot2.shape("square")
bot3.shape("square")
bot4.shape("square")
#Define bot size
sz = 2.1 #2.1
bot1.turtlesize(sz)
bot2.turtlesize(sz)
bot3.turtlesize(sz)
bot4.turtlesize(sz)

#Define pathways for bots
''' Simply change here for a new path'''

bot1_path = ['S1','D1','S1']
bot2_path = ['S2','D2','S2']
bot3_path = ['S3','D3','S3']
bot4_path = ['S4','D4','S4']

#Disable path tracing
bot1.penup()
bot2.penup()
bot3.penup()
bot4.penup()
#Move bots to starting points
bot1.goto(node_translator.node_to_coord(bot1_path[0]))
bot2.goto(node_translator.node_to_coord(bot2_path[0]))
bot3.goto(node_translator.node_to_coord(bot3_path[0]))
bot4.goto(node_translator.node_to_coord(bot4_path[0]))

#Enable path tracing
bot1.pendown()
bot2.pendown()
bot3.pendown()
bot4.pendown()

#Track the locations where the bot have already been
bot1_path_index = 1
bot2_path_index = 1
bot3_path_index = 1
bot4_path_index = 1
bot1_target = bot1_path[bot1_path_index]
bot2_target = bot2_path[bot2_path_index]
bot3_target = bot3_path[bot3_path_index]
bot4_target = bot4_path[bot4_path_index]

quickness = 0
while True:
    #Get current position of bots
    '''This section simulates what the video processing must do'''
    bot1_coords = bot1.position()
    bot2_coords = bot2.position()
    bot3_coords = bot3.position()
    bot4_coords = bot4.position()

    #now find what nodes they are at
    bot1_currentnode = node_translator.coord_to_node(bot1_coords)
    bot2_currentnode = node_translator.coord_to_node(bot2_coords)
    bot3_currentnode = node_translator.coord_to_node(bot3_coords)
    bot4_currentnode = node_translator.coord_to_node(bot4_coords)

    #Now find where they should go
    if bot1_currentnode == bot1_path[bot1_path_index]:
        #Bot has arrived at one check point
        ''' Include here, any specific actions at the checkpoint '''
        bot1_path_index = bot1_path_index + 1
        try:
            bot1_target = bot1_path[bot1_path_index]
        except IndexError:
            bot1_path_index = bot1_path_index - 1
            print("Bot 1 has already reached final destination")
    if bot2_currentnode == bot2_path[bot2_path_index]:
        #Bot has arrived at one check point
        ''' Include here, any specific actions at the checkpoint '''
        bot2_path_index = bot2_path_index + 1
        try:
            bot2_target = bot2_path[bot2_path_index]
        except IndexError:
            bot2_path_index = bot2_path_index - 1
            print("Bot 2 has already reached final destination")
    if bot3_currentnode == bot3_path[bot3_path_index]:
        #Bot has arrived at one check point
        ''' Include here, any specific actions at the checkpoint '''
        bot3_path_index = bot3_path_index + 1
        try:
            bot3_target = bot3_path[bot3_path_index]
        except IndexError:
            bot3_path_index = bot3_path_index - 1
            print("Bot 3 has already reached final destination")
    if bot4_currentnode == bot4_path[bot4_path_index]:
        #Bot has arrived at one check point
        ''' Include here, any specific actions at the checkpoint '''
        bot4_path_index = bot4_path_index + 1
        try:
            bot4_target = bot4_path[bot4_path_index]
        except IndexError:
            bot4_path_index = bot4_path_index - 1
            print("Bot 4 has already reached final destination")

    #Now the swarm algorithm must tell how to Move
    [bot1_nextnode,bot2_nextnode,bot3_nextnode,bot4_nextnode] = swarm_algo.swarm_algo(bot1_currentnode,bot1_target,
                                                                                    bot2_currentnode,bot2_target,
                                                                                    bot3_currentnode,bot3_target,
                                                                                    bot4_currentnode,bot4_target)

    #Move accordingly
    '''This is where the bots are instructed via WiFi'''
    bot1.goto(node_translator.node_to_coord(bot1_nextnode))
    bot2.goto(node_translator.node_to_coord(bot2_nextnode))
    bot3.goto(node_translator.node_to_coord(bot3_nextnode))
    bot4.goto(node_translator.node_to_coord(bot4_nextnode))
    quickness = quickness + 1
    print("Time Elapsed: " + str(quickness))
    #Wait for 0.1 seconds
    #time.sleep(0.1)

arena.mainloop()
