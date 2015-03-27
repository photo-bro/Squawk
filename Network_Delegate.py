###################################################
#                                                 #
#   _____                                 _       #
#  /  ___|                               | |      #
#  \ `--.   __ _  _   _   __ _ __      __| | __   #
#   `--. \ / _` || | | | / _` |\ \ /\ / /| |/ /   #
#  /\__/ /| (_| || |_| || (_| | \ V  V / |   <    #
#  \____/  \__, | \__,_| \__,_|  \_/\_/  |_|\_\   #
#             | |                                 #
#             |_|                                 #
#  Network_Delegate.py                            #
#                                                 #
#  Course: CSCI 333 Networking                    #
#  Professor: John Broere                         #
#  Author: Josh Harmon                            #
#  Created: 3/5/15                                #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
###################################################

# System imports
import socket

class Peer:
    
    __Addr = ""
    __Port = -1
    __Name = ""
    
    def __init__(self, addr, port, name):
        # Bring globals into scope
        global __Addr
        global __Port
        global __Name
        
        # Assign values from constructor
        __Addr = addr
        __Port = int(port)
        __Name = name

        
    def getAddress(self):
        #print ((__Addr, __Port))    #trace
        return (__Addr, __Port)

    def getPort(self):
        return __Port
    
    #######################
    # Pre: None
    # Return: String as: "name at: address:port"
    def __str__(self):
        # if not __Addr or not __Port or not __Name:
        #    return "Not Instantiated"
        return str.format("{0} at: {1}:{2}", __Name, __Addr, __Port)

class Network_Connector:
    
    ################
    # C L A S S    D A T A 
    ###############
    #print("NetDel Data!")   #trace
    global __isConnected
    global __outSocket
    global __activePeer
    __isConnected = False
    __outSocket = None
    __activePeer = None
    
    ################
    # P R I V A T E   F U N C T I O N S
    ###############
    def __init__(self):
        pass
    
    def __Handshake(self, Peer):
        pass
    
    ################
    # P U B L I C   F U N C T I O N S
    ###############
    
    #######################
    # Description: Attempt to connect to address:port
    # Pre: None
    # Return: True if conection successful, False if not
    def TryConnection(self, Peer):
        # Bring Globals into current scope to be able to modify their values
        global __isConnected
        global __outSocket
        global __activePeer
                
        # Check if there is an active peer
        if (not __activePeer) or (__activePeer != Peer):
            __activePeer = Peer
        #print(__activePeer)  #trace
        
        # Create and setup socket
        try:
            __outSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # Create Datagram Socket (UDP)
            __outSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Make Socket Reuseable
            __outSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Allow incoming broadcasts
            __outSocket.setblocking(False)                                     # Set socket to non-blocking mode
            __outSocket.bind(('', __activePeer.getPort()))                     # Accept Connections on port
            __isConnected = True
        except:
            Exception
            # socket creation failed
            __isConnected = False
            
        return __isConnected
    
    #######################
    # Pre: None
    # Return: True if object is connected, False if not
    def isConnected(self):
        return __isConnected
    
    #######################
    # Pre: Must be connected
    # Return: Message has been set
    def SendMessage(self, message):
        # Check connection
        if  __isConnected == False:
            return False
        # Send message
        __outSocket.sendto(bytes(message, 'utf-8'), __activePeer.getAddress())

        
    #######################
    # Pre: Must be connected
    # Return: Messages from Peer
    def GetMessages(self):
        # Check connection
        if  __isConnected == False:
            return False
        
        # get message
        message, address = __outSocket.recvfrom(8192)
        
        # return message if not empty
        if message:
            #print("--There is a message") #trace
            return (message, address) 
        
    #######################
    # Pre: None
    # Return: Connection and object status returned
    def Info(self):
        return str.format("Connected to {0}", __activePeer)
    
        
    