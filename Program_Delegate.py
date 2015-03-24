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
#  Program_Delegate.py                            #
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
import time, threading
from datetime import datetime


# Local imports
import Network_Delegate
import CLI
#import Log

# Concept and code credit:
# http://code.activestate.com/recipes/578591-primitive-peer-to-peer-chat/
class InputThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = 1
    
    def run(self):
        while self.running:
            outMessage =  input("=] ")
            if outMessage:                           
                # Don't send empty message
                try:
                    m_NC.SendMessage(outMessage)
                except:
                    Exception
            time.sleep(0.1)
                
    
    def kill(self):
        self.running = 0

class ReceiveThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = 1
    
    def run(self):
        while self.running:
            try:
                inMessage, (inIP, inPort) = Network_Delegate.Network_Connector().GetMessages()
                if inMessage != False:
                    # print Peer information and message received time
                    ct = datetime.today().time()
                    print(str.format("{0}:{1} at {3}:{4}:{5} => {2}", inIP, inPort, inMessage.decode("utf-8"), ct.hour, ct.minute, ct.second))
            except:
                #print("***No new messages")   #trace
                pass
            time.sleep(0.1)
                
    
    def kill(self):
        self.running = 0
    
class Program:
    
    # Class objects
    global m_CLI
    global m_NC
    m_CLI = CLI.UI()
    m_NC = Network_Delegate.Network_Connector()
    
    def ProgramEntry(self):
        
        # Draw menu
        m_CLI.DrawMainMenu()
        #print(sys.stdout.encoding)
        
        # Prompt for peer information
        peer = m_CLI.PeerInfoPrompt()

        # Try connection
        while (not m_NC.TryConnection(peer) ):
            print("Connection Failed. Try again or type \"quit\" to quit :")
            # Prompt for peer information
            peer = m_CLI.PeerInfoPrompt()
                
        # Print successful connection    
        print(m_NC.Info())
               
               
        #print(str.format("Active Threads: {0}", threading.active_count())) # trace
        
        # Setup message retrieve thread
        getMessages = ReceiveThread()
        getMessages.start()
        
        # Setup input thread
        userInput = InputThread()
        userInput.start()
        
        #print(str.format("Active Threads: {0}", threading.active_count())) # trace
        
        running = True
        while running:
            pass
#            
            # Draw screen
            #m_CLI.DrawChat()
            
        getMessages.kill()
        userInput.kill()
            
        # Exit on disconnect
        quit()
        
        

# Star program
if __name__ == "__main__":
    Program.ProgramEntry(None)