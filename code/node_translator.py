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
lookup_table = {'D1':(),'D2','D3','D4','S1':(-72.5,215.5),'S2','S3','S4','A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4','E1','E2','E3','E4','F1','F2','F3','F4','G1','G2','G3','G4','H1','H2','H3','H4','J1','J2','J3','J4','J5','J6','J7','J8','J9','J10','J11','J12','J13','J14','J15','J16','K1','K2','K3','K4','K5','K6','K7','K8','K9','K10','K11','K12','K13','K14','K15','K16'}

#The translator should approximate the location
#The coordinates won't always match the set value, so may be run an MSE to find best match
def coord_to_node(x_coord,y_coord) :
    coords = (x_coord,y_coord)

    node = ??
    return node

#The other way
def node_to_coord(node):
    coords = lookup_table[node]
    return coords
