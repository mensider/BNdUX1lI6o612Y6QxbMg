#I am going to use the lookup table approach to make everything faster
#Yeah it is tiresome to make the table at first
#But it is a one-time process

#These are the parameters for current arena
'''
arena_origin_y = 215.5
arena_origin_x = -72.5
arena_blocksize = 47.5
'''

#The table must be generated each time for a new arena, but not for new bot pathways.
#This time I did it by hand, may be I should write a function next time
lookup_table = {'D1':(-405,-164.5),'D2':(-405,-212),'D3':(402.5,-212),'D4':(402.5,-164.5),
                'S1':(-72.5,215.5),'S2':(-25,215.5),'S3':(22.5,215.5),'S4':(70,215.5),
                'A1':(-72.5,168),'A2':(-25,168),'A3':(22.5,168),'A4':(70,168),
                'B1':(-72.5,120.5),'B2':(-25,120.5),'B3':(22.5,120.5),'B4':(70,120.5),
                'C1':(-72.5,73),'C2':(-25,73),'C3':(22.5,73),'C4':(70,73),
                'E1':(-72.5,25.5),'E2':(-25,25.5),'E3':(22.5,25.5),'E4':(70,25.5),
                'F1':(-72.5,-22),'F2':(-25,-22),'F3':(22.5,-22),'F4':(70,-22),
                'G1':(-72.5,-69.5),'G2':(-25,-69.5),'G3':(22.5,-69.5),'G4':(70,-69.5),
                'H1':(-72.5,-117),'H2':(-25,-117),'H3':(22.5,-117),'H4':(70,-117),
                'J1':(-357.5,-164.5),'J2':(-310,-164.5),'J3':(-262.5,-164.5),'J4':(-215,-164.5),
                'J5':(-167.5,-164.5),'J6':(-120,-164.5),'J7':(-72.5,-164.5),'J8':(-25,-164.5),
                'J9':(22.5,-164.5),'J10':(70,-164.5),'J11':(117.5,-164.5),'J12':(165,-164.5),
                'J13':(212.5,-164.5),'J14':(260,-164.5),'J15':(307.5,-164.5),'J16':(355,-164.5),
                'K1':(-357.5,-212),'K2':(-310,-212),'K3':(-262.5,-212),'K4':(-215,-212),
                'K5':(-167.5,-212),'K6':(-120,-212),'K7':(-72.5,-212),'K8':(-25,-212),
                'K9':(22.5,-212),'K10':(70,-212),'K11':(117.5,-212),'K12':(165,-212),
                'K13':(212.5,-212),'K14':(260,-212),'K15':(307.5,-212),'K16':(355,-212)}

#The translator should approximate the location
#The coordinates won't always match the set value, so may be run an MSE to find best match
def coord_to_node(x_coord,y_coord) :
    bot_coords = (x_coord,y_coord)
    MSE = 1000 #an arbitrary value that is very high
    for node_current,coords in lookup_table.items():
        MSE_current = (((bot_coords[0] - coords [0])*(bot_coords[0] - coords [0])) + ((bot_coords[1] - coords [1])*(bot_coords[1] - coords [1])))/2
        if MSE_current < MSE :
            node = node_current
    return node

#The other way
def node_to_coord(node):
    coords = lookup_table[node]
    return coords
