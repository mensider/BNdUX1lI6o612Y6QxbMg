### There are 4 bots. Two induct zones. 'Z5' and 'Z10' are induct zones.
### Instruction Pipeline: Image Processing -> Swarm -> WiFi command center -> Bots
### Image Processing gives real time coordinates of 4 bots.
### Swarm gives instantaneous directions for 4 bots.
### Excel file gives the destination for 2 bots in the induct zones.
### Bot tray one direction only.

destination_dict = {0:"NotDefined",1:"Mumbai",2:"Delhi",3:"Kolkata",4:"Chennai",5:"Bengaluru",6:"Hyderabad",7:"Pune",8:"Ahemdabad",9:"Jaipur"}
movement_dict = {0:"NotDefined",1:"GoForward",2:"TurnLeftGoForward",3:"TurnRightGoForward",4:"Turn180GoForward"}
class bot:
    package_loaded = False
    destination_city = 0
    destination_node = "NotDefined"
    current_location = "NotDefined"
    movement = 0

    def __init__(self, name):
        self.name = name

    def get_destination(self):
        #self.destination_city = pipe from excel reader
        pass

    def get_current(self):
        #self.current_location = pipe from img Processing
        pass

    def print_status(self):
        print("Name: ", self.name)
        print("Destination: ", destination_dict[self.destination])
        print("Location: ", self.current_location)
        print("Instruction: ", movement_dict[self.movement])
        print("---------------------------------------------------")

bot1 = bot('RED')
bot2 = bot('BLUE')
bot3 = bot('YELLOW')
bot4 = bot('GREEN')
bot1.print_status()
bot2.print_status()
bot3.print_status()
bot4.print_status()

while True: #Runs indefinitely
    #Get current location of all bots
    bot1.get_current()
    bot2.get_current()
    bot3.get_current()
    bot4.get_current()

    #Check if any bot not loaded
    if(bot1.package_loaded == False):
        if(bot1.current_location == 'Z5' or bot1.current_location == 'Z10'):    #Check in induct zone
            bot1.get_destination()
            bot1.destination_node = destination_calculator (bot1)
            bot1.package_loaded = True
    if(bot2.package_loaded == False):
        if(bot2.current_location == 'Z5' or bot2.current_location == 'Z10'):    #Check in induct zone
            bot2.get_destination()
            bot2.destination_node = destination_calculator (bot2)
            bot2.package_loaded = True
    if(bot3.package_loaded == False):
        if(bot3.current_location == 'Z5' or bot3.current_location == 'Z10'):    #Check in induct zone
            bot3.get_destination()
            bot3.destination_node = destination_calculator (bot3)
            bot3.package_loaded = True
    if(bot4.package_loaded == False):
        if(bot4.current_location == 'Z5' or bot4.current_location == 'Z10'):    #Check in induct zone
            bot4.get_destination()
            bot4.destination_node = destination_calculator (bot4)
            bot4.package_loaded = True

    #Check if bot reached its destination
    if(bot1.current_location == bot1.destination_node):
        wifi_command(flip_bot1)                     #deliver package
        bot1.package_loaded = False
        if(bot1.destination_city in [1,2,3,5,6]):   #choose the nearest induct zone to return
            bot1.destination_node = 'Z5'
        else:
            bot1.destination_node = 'Z10'
    if(bot2.current_location == bot2.destination_node):
        wifi_command(flip_bot2)                     #deliver package
        bot2.package_loaded = False
        if(bot2.destination_city in [1,2,3,5,6]):   #choose the nearest induct zone to return
            bot2.destination_node = 'Z5'
        else:
            bot2.destination_node = 'Z10'
    if(bot3.current_location == bot3.destination_node):
        wifi_command(flip_bot1)                     #deliver package
        bot3.package_loaded = False
        if(bot3.destination_city in [1,2,3,5,6]):   #choose the nearest induct zone to return
            bot3.destination_node = 'Z5'
        else:
            bot3.destination_node = 'Z10'
    if(bot4.current_location == bot4.destination_node):
        wifi_command(flip_bot1)                     #deliver package
        bot4.package_loaded = False
        if(bot4.destination_city in [1,2,3,5,6]):   #choose the nearest induct zone to return
            bot4.destination_node = 'Z5'
        else:
            bot4.destination_node = 'Z10'

    #Pass the locations to swarm algorithm
    [bot1.movement,bot2.movement,bot3.movement,bot4.movement] = swarm_algorithm(bot1.current_location,bot1.destination_node,bot2.current_location,bot2.destination_node,bot3.current_location,bot3.destination_node,bot4.current_location,bot4.destination_node)
    #Pass instructions to Wifi command center
    wifi_command(bot1.movement,bot2.movement,bot3.movement,bot4.movement)

    #Finally print status
    bot1.print_status()
    bot2.print_status()
    bot3.print_status()
    bot4.print_status()

print("[--] Exited Main Loop [--]")

#destination_dict = {0:"NotDefined",1:"Mumbai",2:"Delhi",3:"Kolkata",4:"Chennai",5:"Bengaluru",6:"Hyderabad",7:"Pune",
#8:"Ahemdabad",9:"Jaipur"}, Just for Reference
def destination_calculator(botx):   #now we use predefined dictionary mapping, later we can add dynamic destinations
    destination_map_1 = {1:'B4',2:'F4',3:'J4',4:'B7',5:'F7',6:'J7',7:'C10',8:'G10',9:'K10'}  #from induct zone 'Z5'
    destination_map_2 = {1:'C5',2:'G5',3:'K5',4:'B8',5:'F8',6:'J8',7:'B11',8:'F11',9:'J11'}  #from induct zone 'Z10'
    if botx.current_location == 'Z5':
        return destination_map_1[botx.destination_city]
    if botx.current_location == 'Z10':
        return destination_map_2[botx.destination_city]

def swarm_algorithm(b1_curr,b1_dst,b2_curr,b2_dst,b3_curr,b3_dst,b4_curr,b4_dst):
    ''' To proceed, define the network, nodes, and direction of motion bw nodes. '''
    return [b1_mov,b2_mov,b3_mov,b4_mov]
