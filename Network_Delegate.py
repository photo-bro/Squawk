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
    
    def __init__(self, addr, port, name = "none"):
        # Assign values from constructor
        self.__Addr = addr
        self.__Port = int(port)
        self.__peerName = name

    def getAddress(self):
        return (self.__Addr, self.__Port)

    def getPort(self):
        return self.__Port
    
    #######################
    # Pre: None
    # Return: String as: "name at: address:port"
    def __str__(self):
        # if not __Addr or not __Port or not __peerName:
        #    return "Not Instantiated"
        return str.format("{0} at: {1}:{2}", self.__peerName, self.__Addr, self.__Port)

class Network_Connector:
    
    ################
    # C L A S S    D A T A 
    ###############
    __isConnected = False
    __outSocket = None
    __activePeer = None
    
    ################
    # P R I V A T E   F U N C T I O N S
    ###############
    def __init__(self):
        pass
    
    
    ################
    # P U B L I C   F U N C T I O N S
    ###############
    
    #######################
    # Description: Attempt to connect to address:port
    # Pre: None
    # Return: True if conection successful, False if not
    def TryConnection(self, Peer):
        # Check if there is an active peer
        if (not self.__activePeer) or (self.__activePeer != Peer):
            self.__activePeer = Peer
        #print(__activePeer)  #trace
        
        # Create and setup socket
        try:
            self.__outSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # Create Datagram Socket (UDP)
            self.__outSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Make Socket Reuseable
            self.__outSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Allow incoming broadcasts
            self.__outSocket.setblocking(False)                                     # Set socket to non-blocking mode
            self.__outSocket.bind(('', self.__activePeer.getPort()))                     # Accept Connections on port
            self.__isConnected = True
        except:
            Exception
            # socket creation failed
            self.__isConnected = False
            
        return self.__isConnected
    
    
    # Handshake Format:
    # Client Username  
    def Handshake(self, local_handle):
        global __activePeer
        # Check connection
        if  self.__isConnected == False:
            pass
        
        # Send info
        msg = local_handle
        self.__outSocket.sendto(bytes(msg, 'utf-8'), self.__activePeer.getAddress())
        self.__outSocket.sendto(bytes("BEGIN", 'utf-8'), self.__activePeer.getAddress())

        # Wait for info
        getMessage, getAddress = self.__outSocket.recvfrom(8192)
        
        # Assign name
        __activePeer.__peerName = getMessage.decode("utf-8")
        print(__activePeer.__peerName) #trace
        
    
    
    #######################
    # Pre: None
    # Return: True if object is connected, False if not
    def isConnected(self):
        return self.__isConnected
    
    #######################
    # Pre: Must be connected
    # Return: Message has been set
    def SendMessage(self, message):
        # Check connection
        if  self.__isConnected == False:
            return False
        # Send message
        self.__outSocket.sendto(bytes(message, 'utf-8'), self.__activePeer.getAddress())

        
    #######################
    # Pre: Must be connected
    # Return: Messages from Peer
    def GetMessages(self):
        # Check connection
        if  self.__isConnected == False:
            return False
        
        # get message
        message, address = self.__outSocket.recvfrom(8192)
        
        # return message if not empty
        if message:
            #print("--There is a message") #trace
            return (message, address) 
        
    #######################
    # Pre: None
    # Return: Connection and object status returned
    def Info(self):
        return str.format("Connected to {0}", self.__activePeer)
    
        
    