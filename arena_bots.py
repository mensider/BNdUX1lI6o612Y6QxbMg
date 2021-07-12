# The Plan
# --------
# [.] Use an image of the arean as background
# [.] Define 4 rect blocks, each for a bot
# [.] Assume a precursor fn which will provide coordinates of each bot

# [.] Go Plan Epsilon

import turtle

#Setup the Arena
arena=turtle.Screen()
arena.bgpic(picname="Arena.png")
arena.setup(width=1000,height=480)
arena_origin_y = 215.5
arena_origin_x = -72.5
arena_blocksize = 47.5
#Define bot objects
bot1 = turtle.Turtle()
bot2 = turtle.Turtle()
bot3 = turtle.Turtle()
bot4 = turtle.Turtle()
#Define bot colors
bot1.color("white")
bot2.color("green")
bot3.color("red")
bot4.color("blue")
#Define bot shapes
bot1.shape("square")
bot2.shape("square")
bot3.shape("square")
bot4.shape("square")
#Define bot size
bot1.turtlesize(2.1)
bot2.turtlesize(2.1)
bot3.turtlesize(2.1)
bot4.turtlesize(2.1)
#Disable path tracing
bot1.penup()
bot2.penup()
bot3.penup()
bot4.penup()
#Move bots to starting points
bot1.goto(arena_origin_x,arena_origin_y)
bot2.goto(arena_origin_x+arena_blocksize,arena_origin_y)
bot3.goto(arena_origin_x+(2*arena_blocksize),arena_origin_y)
bot4.goto(arena_origin_x+(3*arena_blocksize),arena_origin_y)
#Enable path tracing
bot1.pendown()
bot2.pendown()
bot3.pendown()
bot4.pendown()

for i in range(1,100):
    #Get current position of bots
    #This section simulates what the video processing must do
    bot1_coords = bot1.position()
    bot1_x = bot1_coords[0]
    bot1_y = bot1_coords[1]
    print(bot1_x,bot1_y)
    bot2_coords = bot2.position()
    bot2_x = bot2_coords[0]
    bot2_y = bot2_coords[1]
    bot3_coords = bot3.position()
    bot3_x = bot3_coords[0]
    bot3_y = bot3_coords[1]
    bot4_coords = bot4.position()
    bot4_x = bot4_coords[0]
    bot4_y = bot4_coords[1]

    #Now the swarm algorithm must tell how to Move
    [bot1_dx,bot1_dy, bot2_dx,bot2_dy, bot3_dx,bot3_dy, bot4_dx,bot4_dy] = swarm_algo(bot1_x,bot1_y , bot2_x,bot2_y , bot3_x,bot3_y , bot4_x,bot4_y)

    #Move accordingly
    bot1.goto(bot1_x + bot1_dx , bot1_y + bot1_dy)
    bot2.goto(bot2_x + bot2_dx , bot2_y + bot2_dy)
    bot3.goto(bot3_x + bot3_dx , bot3_y + bot3_dy)
    bot4.goto(bot4_x + bot4_dx , bot4_y + bot4_dy)

arena.mainloop()
