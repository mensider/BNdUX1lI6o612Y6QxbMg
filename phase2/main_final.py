""" # There are 4 bots. Two induct zones. 'Z5' and 'Z10' are induct zones.
    # Instruction Pipeline: Image Processing -> Swarm -> WiFi command center -> Bots
    # Image Processing gives real time coordinates of 4 bots.
    # Swarm gives instantaneous directions for 4 bots.
    # Excel file gives the destination for 2 bots in the induct zones.
    # Bot tray one direction only. """

import networkx as nx
import pandas as pd
import socket
import time

def parseCsv(fileloc):
    # Reading the csv file
    df =pd.read_excel(fileloc)
    induct_st_1 = []
    induct_st_2 = []
    # Extracting out only the required columns
    df = df[['Shipment', 'Induct Station', 'Destination']].copy()
    i = 0
    for row in df['Induct Station']:
        if row==1:
            induct_st_1.append(df['Destination'][i])
        if row ==2:
            induct_st_2.append(df['Destination'][i])
        i = i+1

    return (induct_st_1,induct_st_2)

(induct_st_1,induct_st_2) = parseCsv('./Sample_Data_latest.xlsx')
#print(induct_st_1['key'][index])

#Dictionaries
destination_dict = {0:"NotDefined",1:"Mumbai",2:"Delhi",3:"Kolkata",4:"Chennai",5:"Bengaluru",6:"Hyderabad",\
                    7:"Pune",8:"Ahemdabad",9:"Jaipur"}
movement_dict = {0:"NotDefined",1:"GoForward",2:"TurnLeftGoForward",3:"TurnRightGoForward",4:"Turn180GoForward"}
orientation_dict={0:"NotDefined",1:"North",2:"East",3:"West",4:"South"}
#Read destination list

pkg_num_in_1 = 0  #packages['Destination'][pkg_num] gives the destination for next package
pkg_num_in_2 = 0
pkg_num =0

def destination_calculator(botx):
    # now we use predefined dictionary mapping, later we can add dynamic destinations
    # destination_dict = {0:"NotDefined",1:"Mumbai",2:"Delhi",3:"Kolkata",4:"Chennai",5:"Bengaluru",6:"Hyderabad",\
    # 7:"Pune", 8:"Ahemdabad",9:"Jaipur"}, Just for Reference
    destination_map_1 = {1:'B4',2:'F4',3:'J4',4:'B7',5:'F7',6:'J7',7:'C10',8:'G10',9:'K10'}  #from induct zone 'Z5'
    destination_map_2 = {1:'C5',2:'G5',3:'K5',4:'B8',5:'F8',6:'J8',7:'B11',8:'F11',9:'J11'}  #from induct zone 'Z10'
    if botx.current_location == 'Z5':
        return destination_map_1[botx.destination_city]
    if botx.current_location == 'Z10':
        return destination_map_2[botx.destination_city]

def movement_direction(bx_curr,bx_next_node,bx_facing):
    bx_mov = 0
    bx_orientation = bx_facing
    # from induct zone
    if(bx_curr == 'Z5' or bx_curr == 'Z10'):
        bx_mov = 1
        bx_orientation = 2
        return bx_mov,bx_orientation

    # split nodes to row and column
    bx_curr_column = ord(bx_curr[0])
    bx_curr_row = int(bx_curr[1:])
    bx_next_node_column = ord(bx_next_node[0])
    bx_next_node_row = int(bx_next_node[1:])

    # if facing east
    if(bx_facing == 2):
        # if moving along the column
        if(bx_curr_column == bx_next_node_column):
            # if moving one row up
            if(bx_curr_row > bx_next_node_row):
                bx_mov = 2
                bx_orientation = 1
                return bx_mov, bx_orientation
            # if moving one row down
            if (bx_curr_row < bx_next_node_row):
                bx_mov = 3
                bx_orientation = 4
                return bx_mov, bx_orientation
        # if moving along the row
        if(bx_curr_row == bx_next_node_row):
            # if moving one column right
            if(bx_curr_column < bx_next_node_column):
                bx_mov = 1
                bx_orientation = 2
                return bx_mov, bx_orientation
            # if moving one column left
            if(bx_curr_column > bx_next_node_column):
                bx_mov = 4
                bx_orientation = 3
                return bx_mov, bx_orientation

    # if facing west
    if (bx_facing == 3):
        # if moving along the column
        if (bx_curr_column == bx_next_node_column):
            # if moving one row up
            if (bx_curr_row > bx_next_node_row):
                bx_mov = 3
                bx_orientation = 1
                return bx_mov, bx_orientation
            # if moving one row down
            if (bx_curr_row < bx_next_node_row):
                bx_mov = 2
                bx_orientation = 4
                return bx_mov, bx_orientation
        # if moving along the row
        if (bx_curr_row == bx_next_node_row):
            # if moving one column right
            if (bx_curr_column < bx_next_node_column):
                bx_mov = 4
                bx_orientation = 2
                return bx_mov, bx_orientation
            # if moving one column left
            if (bx_curr_column > bx_next_node_column):
                bx_mov = 1
                bx_orientation = 3
                return bx_mov, bx_orientation

    # if facing north
    if (bx_facing == 1):
        # if moving along the column
        if (bx_curr_column == bx_next_node_column):
            # if moving one row up
            if (bx_curr_row > bx_next_node_row):
                bx_mov = 1
                bx_orientation = 1
                return bx_mov, bx_orientation
            # if moving one row down
            if (bx_curr_row < bx_next_node_row):
                bx_mov = 4
                bx_orientation = 4
                return bx_mov, bx_orientation
        # if moving along the row
        if (bx_curr_row == bx_next_node_row):
            # if moving one column right
            if (bx_curr_column < bx_next_node_column):
                bx_mov = 3
                bx_orientation = 2
                return bx_mov, bx_orientation
            # if moving one column left
            if (bx_curr_column > bx_next_node_column):
                bx_mov = 2
                bx_orientation = 3
                return bx_mov, bx_orientation

    # if facing south
    if (bx_facing == 4):
        # if moving along the column
        if (bx_curr_column == bx_next_node_column):
            # if moving one row up
            if (bx_curr_row > bx_next_node_row):
                bx_mov = 4
                bx_orientation = 1
                return bx_mov, bx_orientation
            # if moving one row down
            if (bx_curr_row < bx_next_node_row):
                bx_mov = 1
                bx_orientation = 4
                return bx_mov, bx_orientation
        # if moving along the row
        if (bx_curr_row == bx_next_node_row):
            # if moving one column right
            if (bx_curr_column < bx_next_node_column):
                bx_mov = 2
                bx_orientation = 2
                return bx_mov, bx_orientation
            # if moving one column left
            if (bx_curr_column > bx_next_node_column):
                bx_mov = 3
                bx_orientation = 3
                return bx_mov, bx_orientation
    return 0,0

def swarm_algorithm(grid,b1,b2,b3):
    b1_curr = b1.current_location
    b1_dst = b1.destination_node
    b1_facing = b1.orientation
    b2_curr = b2.current_location
    b2_dst = b2.destination_node
    b2_facing = b2.orientation
    b3_curr = b3.current_location
    b3_dst = b3.destination_node
    b3_facing = b3.orientation
    # call networkx function to find shortest path
    bot1_path = nx.bidirectional_shortest_path(grid, b1_curr, b1_dst)
    bot2_path = nx.bidirectional_shortest_path(grid, b2_curr, b2_dst)
    bot3_path = nx.bidirectional_shortest_path(grid, b3_curr, b3_dst)
    # TODO : additional collision detection to be implemented
    bot1_cross1 = False
    bot2_cross1 = False
    bot3_cross1 = False
    # bot4_cross1 = False
    bot1_cross2 = False
    bot2_cross2 = False
    bot3_cross2 = False
    # bot4_cross2 = False
    cross_1 = ['Z5', 'A5', 'B5', 'A4', 'A6']
    cross_2 = ['Z10', 'A10', 'B10', 'A9', 'A11']

    print("Before CDA")
    print("B1 : ", bot1_path)
    print("B2 : ", bot2_path)
    print("B3 : ", bot3_path)
    # print("B4 : ", bot4_path)
    # TODO : Do Deep Runs.. Analyze error codes and remove all possible instance of such errors.
    # Types of collissions:
    # --> Holy cross congestion   (highest priority)
    # --> Head to head collisions (make sure removing a node doesnt creat Islands)
    # --> Common node collissions (make sure removing a node doesnt creat Islands)
    # --> Make sure removing a node doesnt create Islands.
    # --> Use both delays and detours.
    # --> There is a piece of paper with some ideas. Take that and add it here.

    '''0) Holy Cross Congestion '''
    if (bot1_path[1] in cross_1):
        bot1_cross1 = True
    if (bot2_path[1] in cross_1):
        bot2_cross1 = True
    if (bot3_path[1] in cross_1):
        bot3_cross1 = True
    # if (bot4_path[1] in cross_1):
    #    bot4_cross1 = True
    if (bot1_path[1] in cross_2):
        bot1_cross2 = True
    if (bot2_path[1] in cross_2):
        bot2_cross2 = True
    if (bot3_path[1] in cross_2):
        bot3_cross2 = True

    if (bot1_cross1 is True):  # if bot 1 is going into cross 1
        if (bot2_cross1 is True):
            print("1 and 2 : Type 0")
            bot2_path.insert(0, bot2_path[0])  # hold the bot
            print("B2 : ", bot2_path)
        if (bot3_cross1 is True):
            print("1 and 3 : Type 0")
            bot3_path.insert(0, bot3_path[0])  # hold the bot
            print("B3 : ", bot3_path)
    if (bot1_cross2 is True):  # if bot 1 is going into cross 2
        if (bot2_cross2 is True):
            print("1 and 2 : Type 0")
            bot2_path.insert(0, bot2_path[0])  # hold the bot
            print("B2 : ", bot2_path)
        if (bot3_cross2 is True):
            print("1 and 3 : Type 0")
            bot3_path.insert(0, bot3_path[0])  # hold the bot
            print("B3 : ", bot3_path)

    if (bot2_cross1 is True):  # if bot 2 is going into cross 1
        if (bot3_cross1 is True):
            print("2 and 3 : Type 0")
            bot3_path.insert(0, bot3_path[0])  # hold the bot
            print("B3 : ", bot3_path)
    if (bot2_cross2 is True):  # if bot 2 is going to cross 2
        if (bot3_cross2 is True):
            print("2 and 3 : Type 0")
            bot3_path.insert(0, bot3_path[0])  # hold the bot
            print("B3 : ", bot3_path)


    ''' 1) Bots get into same nod '''
    if (bot1_path[1] == bot2_path[1]):
        print("1 and 2 : Type 1")
        try:
            G = grid.copy()  # Bot 2 will re-calculate the shortest path
            G.remove_node(bot1_path[1])  # By removing the busy node from the graph
            bot2_path = nx.bidirectional_shortest_path(G, b2_curr, b2_dst)
            print("B2 : ", bot2_path)
        except:  # if there is not a path possible..
            G = grid.copy()  # Bot 2 will re-calculate the shortest path
            G.remove_node(bot2_path[1])  # By removing the busy node from the graph
            bot1_path = nx.bidirectional_shortest_path(G, b1_curr, b1_dst)
            print("B1 : ", bot1_path)
    if (bot1_path[1] == bot3_path[1]):
        print("1 and 3 : Type 1")
        try:
            G = grid.copy()  # Bot 3 will re-calculate the shortest path
            G.remove_node(bot1_path[1])  # By removing the busy node from the graph
            bot3_path = nx.bidirectional_shortest_path(G, b3_curr, b3_dst)
            print("B3 : ", bot3_path)
        except:  # if there is not a path possible..
            G = grid.copy()  # Bot 3 will re-calculate the shortest path
            G.remove_node(bot3_path[1])  # By removing the busy node from the graph
            bot1_path = nx.bidirectional_shortest_path(G, b1_curr, b1_dst)
            print("B1 : ", bot1_path)

    if (bot2_path[1] == bot3_path[1]):
        print("2 and 3 : Type 1")
        try:
            G = grid.copy()  # Bot 3 will re-calculate the shortest path
            G.remove_node(bot2_path[1])  # By removing the busy node from the graph
            bot3_path = nx.bidirectional_shortest_path(G, b3_curr, b3_dst)
            print("B3 : ", bot3_path)
        except:  # if there is not a path possible..
            G = grid.copy()  # Bot 3 will re-calculate the shortest path
            G.remove_node(bot3_path[1])  # By removing the busy node from the graph
            bot2_path = nx.bidirectional_shortest_path(G, b2_curr, b2_dst)
            print("B2 : ", bot2_path)

    ''' 2) Bots cross head into each other '''
    if (bot1_path[0:2] == bot2_path[1::-1]):
        print("1 and 2 : Type 2")
        G = grid.copy()  # Bot 2 will re-calculate the shortest path
        G.remove_node(bot1_path[0])  # By removing the busy node from the graph
        try:
            bot2_path = nx.bidirectional_shortest_path(G, b2_curr, b2_dst)
            print("B2 : ", bot2_path)
        except:  # if there is not a path possible..
            print("Error 106")
            bot2_path.insert(0, bot2_path[0])  # hold the bot

    if (bot1_path[0:2] == bot3_path[1::-1]):
        print("1 and 3 : Type 2")
        G = grid.copy()  # Bot 3 will re-calculate the shortest path
        G.remove_node(bot1_path[0])  # By removing the busy node from the graph
        try:
            bot3_path = nx.bidirectional_shortest_path(G, b3_curr, b3_dst)
            print("B3 : ", bot3_path)
        except:  # if there is not a path possible..
            print("Error 107")
            bot3_path.insert(0, bot3_path[0])  # hold the bot

    if (bot2_path[0:2] == bot3_path[1::-1]):
        print("2 and 3 : Type 2")
        G = grid.copy()  # Bot 3 will re-calculate the shortest path
        G.remove_node(bot2_path[0])  # By removing the busy node from the graph
        try:
            bot3_path = nx.bidirectional_shortest_path(G, b3_curr, b3_dst)
            print("B3 : ", bot3_path)
        except:  # if there is not a path possible..
            print("Error 109")
            bot3_path.insert(0, bot3_path[0])  # hold the bot

    print("After CDA")
    print("B1 : ", bot1_path)
    print("B2 : ", bot2_path)
    print("B3 : ", bot3_path)
    # print("B4 : ", bot4_path)

    #find immediate next node
    b1_next_node = bot1_path[1]
    b2_next_node = bot2_path[1]
    b3_next_node = bot3_path[1]

    #calculate movement direction
    b1_mov,b1_orien = movement_direction(b1_curr,b1_next_node,b1_facing)
    b2_mov,b2_orien = movement_direction(b2_curr, b2_next_node,b2_facing)
    b3_mov,b3_orien = movement_direction(b3_curr, b3_next_node,b3_facing)
    return [b1_mov,b1_orien,b2_mov,b2_orien,b3_mov,b3_orien]

'''
import matplotlib.pyplot as plt     # only needed for plotting the graph

def visualise_network():
    #Show visually
    grid = grid_graph()
    plt.subplot(121)
    nx.draw(grid, with_labels=True)
    plt.show()
    return
'''

def grid_graph():
    list_of_nodes = ['Z5','Z10',\
    'A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','A13','A14',\
    'B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','B12','B13','B14',\
    'C1','C2','C5','C6','C9','C10','C13','C14',\
    'D1','D2','D5','D6','D9','D10','D13','D14',\
    'E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12','E13','E14',\
    'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14',\
    'G1','G2','G5','G6','G9','G10','G13','G14',\
    'H1','H2','H5','H6','H9','H10','H13','H14',\
    'I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11','I12','I13','I14',\
    'J1','J2','J3','J4','J5','J6','J7','J8','J9','J10','J11','J12','J13','J14',\
    'K1','K2','K5','K6','K9','K10','K13','K14',\
    'L1','L2','L5','L6','L9','L10','L13','L14',\
    'M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12','M13','M14',\
    'N1','N2','N3','N4','N5','N6','N7','N8','N9','N10','N11','N12','N13','N14']

    #No diagonal movement
    list_of_edges=[('Z5','A5'),('Z10','A10'),\
    ('A1','B1'),('A1','A2'),('A2','B2'),('A2','A3'),('A3','B3'),('A3','A4'),('A4','B4'),\
    ('A4','A5'),('A5','B5'),('A5','A6'),('A6','B6'),('A6','A7'),('A7','B7'),('A7','A8'),\
    ('A8','B8'),('A8','A9'),('A9','B9'),('A9','A10'),('A10','B10'),('A10','A11'),\
    ('A11','B11'),('A11','A12'),('A12','B12'),('A12','A13'),('A13','B13'),('A13','A14'),\
    ('A14','B14'),('B1','C1'),('B1','B2'),('B2','C2'),('B2','B3'),('B3','C3'),('B3','B4'),\
    ('B4','C4'),('B4','B5'),('B5','C5'),('B5','B6'),('B6','C6'),('B6','B7'),('B7','C7'),\
    ('B7','B8'),('B8','C8'),('B8','B9'),('B9','C9'),('B9','B10'),('B10','C10'),('B10','B11'),\
    ('B11','C11'),('B11','B12'),('B12','C12'),('B12','B13'),('B13','C13'),('B13','B14'),\
    ('B14','C14'),('C1','D1'),('C1','C2'),('C2','D2'),('C2','C3'),('C3','D3'),('C3','C4'),('C4','D4'),\
    ('C4','C5'),('C5','D5'),('C5','C6'),('C6','D6'),('C6','C7'),('C7','D7'),('C7','C8'),\
    ('C8','D8'),('C8','C9'),('C9','D9'),('C9','C10'),('C10','D10'),('C10','C11'),\
    ('C11','D11'),('C11','C12'),('C12','D12'),('C12','C13'),('C13','D13'),('C13','C14'),\
    ('C14','D14'),('D1','E1'),('D1','D2'),('D2','E2'),('D2','D3'),('D3','E3'),('D3','D4'),('D4','E4'),\
    ('D4','D5'),('D5','E5'),('D5','D6'),('D6','E6'),('D6','D7'),('D7','E7'),('D7','D8'),\
    ('D8','E8'),('D8','D9'),('D9','E9'),('D9','D10'),('D10','E10'),('D10','D11'),\
    ('D11','E11'),('D11','D12'),('D12','E12'),('D12','D13'),('D13','E13'),('D13','D14'),\
    ('D14','E14'),('E1','F1'),('E1','E2'),('E2','F2'),('E2','E3'),('E3','F3'),('E3','E4'),('E4','F4'),\
    ('E4','E5'),('E5','F5'),('E5','E6'),('E6','F6'),('E6','E7'),('E7','F7'),('E7','E8'),\
    ('E8','F8'),('E8','E9'),('E9','F9'),('E9','E10'),('E10','F10'),('E10','E11'),\
    ('E11','F11'),('E11','E12'),('E12','F12'),('E12','E13'),('E13','F13'),('E13','E14'),\
    ('E14','F14'),('F1','G1'),('F1','F2'),('F2','G2'),('F2','F3'),('F3','G3'),('F3','F4'),('F4','G4'),\
    ('F4','F5'),('F5','G5'),('F5','F6'),('F6','G6'),('F6','F7'),('F7','G7'),('F7','F8'),\
    ('F8','G8'),('F8','F9'),('F9','G9'),('F9','F10'),('F10','G10'),('F10','F11'),\
    ('F11','G11'),('F11','F12'),('F12','G12'),('F12','F13'),('F13','G13'),('F13','F14'),\
    ('F14','G14'),('G1','H1'),('G1','G2'),('G2','H2'),('G2','G3'),('G3','H3'),('G3','G4'),('G4','H4'),\
    ('G4','G5'),('G5','H5'),('G5','G6'),('G6','H6'),('G6','G7'),('G7','H7'),('G7','G8'),\
    ('G8','H8'),('G8','G9'),('G9','H9'),('G9','G10'),('G10','H10'),('G10','G11'),\
    ('G11','H11'),('G11','G12'),('G12','H12'),('G12','G13'),('G13','H13'),('G13','G14'),\
    ('G14','H14'),('H1','I1'),('H1','H2'),('H2','I2'),('H2','H3'),('H3','I3'),('H3','H4'),('H4','I4'),\
    ('H4','H5'),('H5','I5'),('H5','H6'),('H6','I6'),('H6','H7'),('H7','I7'),('H7','H8'),\
    ('H8','I8'),('H8','H9'),('H9','I9'),('H9','H10'),('H10','I10'),('H10','H11'),\
    ('H11','I11'),('H11','H12'),('H12','I12'),('H12','H13'),('H13','I13'),('H13','H14'),\
    ('H14','I14'),('I1','J1'),('I1','I2'),('I2','J2'),('I2','I3'),('I3','J3'),('I3','I4'),('I4','J4'),\
    ('I4','I5'),('I5','J5'),('I5','I6'),('I6','J6'),('I6','I7'),('I7','J7'),('I7','I8'),\
    ('I8','J8'),('I8','I9'),('I9','J9'),('I9','I10'),('I10','J10'),('I10','I11'),\
    ('I11','J11'),('I11','I12'),('I12','J12'),('I12','I13'),('I13','J13'),('I13','I14'),\
    ('I14','J14'),('J1','K1'),('J1','J2'),('J2','K2'),('J2','J3'),('J3','K3'),('J3','J4'),('J4','K4'),\
    ('J4','J5'),('J5','K5'),('J5','J6'),('J6','K6'),('J6','J7'),('J7','K7'),('J7','J8'),\
    ('J8','K8'),('J8','J9'),('J9','K9'),('J9','J10'),('J10','K10'),('J10','J11'),\
    ('J11','K11'),('J11','J12'),('J12','K12'),('J12','J13'),('J13','K13'),('J13','J14'),\
    ('J14','K14'),('K1','L1'),('K1','K2'),('K2','L2'),('K2','K3'),('K3','L3'),('K3','K4'),('K4','L4'),\
    ('K4','K5'),('K5','L5'),('K5','K6'),('K6','L6'),('K6','K7'),('K7','L7'),('K7','K8'),\
    ('K8','L8'),('K8','K9'),('K9','L9'),('K9','K10'),('K10','L10'),('K10','K11'),\
    ('K11','L11'),('K11','K12'),('K12','L12'),('K12','K13'),('K13','L13'),('K13','K14'),\
    ('K14','L14'),('L1','M1'),('L1','L2'),('L2','M2'),('L2','L3'),('L3','M3'),('L3','L4'),('L4','M4'),\
    ('L4','L5'),('L5','M5'),('L5','L6'),('L6','M6'),('L6','L7'),('L7','M7'),('L7','L8'),\
    ('L8','M8'),('L8','L9'),('L9','M9'),('L9','L10'),('L10','M10'),('L10','L11'),\
    ('L11','M11'),('L11','L12'),('L12','M12'),('L12','L13'),('L13','M13'),('L13','L14'),\
    ('L14','M14'),('M1','N1'),('M1','M2'),('M2','N2'),('M2','M3'),('M3','N3'),('M3','M4'),('M4','N4'),\
    ('M4','M5'),('M5','N5'),('M5','M6'),('M6','N6'),('M6','M7'),('M7','N7'),('M7','M8'),\
    ('M8','N8'),('M8','M9'),('M9','N9'),('M9','M10'),('M10','N10'),('M10','M11'),\
    ('M11','N11'),('M11','M12'),('M12','N12'),('M12','M13'),('M13','N13'),('M13','M14'),\
    ('M14','N14'),('N1','N2'),('N2','N3'),('N3','N4'),('N4','N5'),('N5','N6'),('N6','N7'),\
    ('N7','N8'),('N8','N9'),('N9','N10'),('N10','N11'),('N11','N12'),('N12','N13'),('N13','N14')]

    #graph setup
    grid = nx.Graph()
    grid.add_nodes_from(list_of_nodes)
    grid.add_edges_from(list_of_edges)
    return grid

# A simple reverse dictionary lookup code snippet
def get_key(val,dictionary):
    for key, value in dictionary.items():
         if val == value:
             return key

def wireless_command(ip,data):
    port = 5000
    ipAddress = '192.168.43.220'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipAddress, port))
    while True:
        data = input("Enter Command: ")
        if (data == 'X'):
            break
        dataBytes = data.encode('utf-8')
        s.send(dataBytes)
        time.sleep(0.000005)
        print(s.recv(1024).decode())

    s.close()

#Get network
grid = grid_graph()

class bot:
    package_loaded = False
    destination_city = 0
    destination_node = "NotDefined"
    current_location = "NotDefined"
    movement = 0
    orientation = 0
    def __init__(self, name):
        self.name = name

    def get_destination(self, city):
        self.destination_city = city
        pass

    def get_current(self, location):
        self.current_location = location
        pass

    def print_status(self):
        print("Name: ", self.name)
        print("Destination: ", destination_dict[self.destination_city])
        print("Location: ", self.current_location)
        print("Orientation: ",orientation_dict[self.orientation])
        print("Instruction: ", movement_dict[self.movement])
        print("---------------------------------------------------")

bot1 = bot('RED')
bot2 = bot('BLUE')
bot3 = bot('GREEN')
bot1.print_status()
bot2.print_status()
bot3.print_status()

while True: #Runs indefinitely
    #Get current location of all bots
    # TODO : connect with IP code
    bot1.get_current(location)
    bot2.get_current(location)
    bot3.get_current(location)

    #Check if any bot not loaded
    if(bot1.package_loaded == False):
        if (bot1.current_location == 'Z5'):  # Check in induct zone 1
            bot1.get_destination(get_key(induct_st_1[pkg_num_in_1], destination_dict))
            bot1.destination_node = destination_calculator(bot1)
            bot1.package_loaded = True
            pkg_num_in_1 = pkg_num_in_1 + 1

        if (bot1.current_location == 'Z10'):  # Check in induct zone 2
            bot1.get_destination(get_key(induct_st_2[pkg_num_in_2], destination_dict))
            bot1.destination_node = destination_calculator(bot1)
            bot1.package_loaded = True
            pkg_num_in_2 = pkg_num_in_2 + 1

    if(bot2.package_loaded == False):
        if(bot2.current_location == 'Z5'):    #Check in induct zone 1
            bot2.get_destination(get_key(induct_st_1[pkg_num_in_1],destination_dict))
            bot2.destination_node = destination_calculator (bot2)
            bot2.package_loaded = True
            pkg_num_in_1 = pkg_num_in_1 + 1

        if (bot2.current_location == 'Z10'):  # Check in induct zone 2
            bot2.get_destination(get_key(induct_st_2[pkg_num_in_2], destination_dict))
            bot2.destination_node = destination_calculator(bot2)
            bot2.package_loaded = True
            pkg_num_in_2 = pkg_num_in_2 + 1

    if(bot3.package_loaded == False):
        if(bot3.current_location == 'Z5'):    #Check in induct zone 1
            bot3.get_destination(get_key(induct_st_1[pkg_num_in_1],destination_dict))
            bot3.destination_node = destination_calculator (bot3)
            bot3.package_loaded = True
            pkg_num_in_1 = pkg_num_in_1 + 1

        if (bot3.current_location == 'Z10'):  # Check in induct zone 2
            bot3.get_destination(get_key(induct_st_2[pkg_num_in_2], destination_dict))
            bot3.destination_node = destination_calculator(bot3)
            bot3.package_loaded = True
            pkg_num_in_2 = pkg_num_in_2 + 1

    #Check if bot reached its destination
    if(bot1.current_location == bot1.destination_node):
        ## wifi_command(flip_bot1)                     #deliver package
        bot1.package_loaded = False
        if(bot1.destination_city in [1,2,3,5,6]):   #choose the nearest induct zone to return
            bot1.destination_node = 'Z5'
        else:
            bot1.destination_node = 'Z10'
    if(bot2.current_location == bot2.destination_node):
        ## wifi_command(flip_bot2)                     #deliver package
        bot2.package_loaded = False
        if(bot2.destination_city in [1,2,3,5,6]):   #choose the nearest induct zone to return
            bot2.destination_node = 'Z5'
        else:
            bot2.destination_node = 'Z10'
    if(bot3.current_location == bot3.destination_node):
        ## wifi_command(flip_bot1)                     #deliver package
        bot3.package_loaded = False
        if(bot3.destination_city in [1,2,3,5,6]):   #choose the nearest induct zone to return
            bot3.destination_node = 'Z5'
        else:
            bot3.destination_node = 'Z10'

    #Pass the locations to swarm algorithm
    [bot1.movement,bot1.orientation,bot2.movement,bot2.orientation,bot3.movement,\
     bot3.orientation]=swarm_algorithm(grid,bot1,bot2,bot3)
    #Pass instructions to Wifi command center
    wireless_command(bot1_ip, bot1.movement)
    wireless_command(bot2_ip, bot2.movement)
    wireless_command(bot3_ip, bot3.movement)
    #TODO: Change the .ino file according to movement_dict

    #Finally print status
    bot1.print_status()
    bot2.print_status()
    bot3.print_status()

print("[--] Exited Main Loop [--]")
