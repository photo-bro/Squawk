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
#  Main.py                                        #
#                                                 #
#  Course: CSCI 333 Networking                    #
#  Professor: John Broere                         #
#  Author: Josh Harmon                            #
#  Created: 4/24/15                               #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
###################################################

# System imports
import time, threading, os, sys
from datetime import datetime

# Local imports
import Network_Delegate, IO_Delegate
import CLI
import Morse

import pdb #debug


################
# Creates separate thread for user input to prevent blocking
#
# Concept and code credit:
# http://code.activestate.com/recipes/578591-primitive-peer-to-peer-chat/
class InputThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = 1
        self.GP = IO_Delegate.GPIO_Delegate()
        self.M = Morse.Morse()
    
    def run(self):
        while self.running:
            outMessage =  input("] ")
            if outMessage:       
                # easy exit    
                if outMessage == "quit":
                    quit()                
                # Don't send empty message
                try:
                    #pdb.set_trace()
                    morse = self.M.TextToMorse(outMessage)
                    print(morse)  # trace
                    self.GP.SendMorse(morse)
                except:
                    Exception
            time.sleep(0.1)
                
    def kill(self):
        self.running = 0

################
# Creates separate thread for printing incoming messages
#
# Concept and code credit:
# http://code.activestate.com/recipes/578591-primitive-peer-to-peer-chat/
class ReceiveThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = 1
        self.GP = IO_Delegate.GPIO_Delegate()
        self.M = Morse.Morse()
    
    def run(self):
        while self.running:                # Check for messages
            inMorse = self.GP.ReceiveMorse()
            if inMorse != None:
                # print Peer information and message received time
                ct = datetime.today().time()
                msg = self.M.MorseToText(inMorse)
                print(str.format("{0}: {1}\n{2}", ct, inMorse, msg))
            time.sleep(0.1)       
    
    def kill(self):
        self.running = 0
        
def Program(self):
    
    # Draw menu
    CLI.UI().DrawMainMenu()
    
    # print(str.format("Active Threads: {0}", threading.active_count())) # trace
        
    # Setup message retrieve thread
    getMessages = ReceiveThread()
    getMessages.start()
    
    # Setup input thread
    userInput = InputThread()
    userInput.start()
    
    # print(str.format("Active Threads: {0}", threading.active_count())) # trace
    
    running = True
    while running:
        time.sleep(5) # no need to run endlessly
        pass
#            
        # Draw screen
        #m_CLI.DrawChat()
        
    getMessages.kill()
    userInput.kill()
        
    # Exit on disconnect
    quit()

# Start program
if __name__ == "__main__":
    Program(None) 
    
    
    
    
    