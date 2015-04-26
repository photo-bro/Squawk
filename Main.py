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
        self.IO = IO_Delegate.IO_Delegate()
        self.M = Morse.Morse()
    
    def run(self):
        while self.running:
            outMessage =  input("] ")
            if outMessage:       
                # easy exit    
                if outMessage == "quit":
                    os._exit(1)                
                # Don't send empty message
                try:
                    #pdb.set_trace()
                    morse = self.M.TextToMorse(outMessage)
                    print(str.format("Sending message: {0}", morse))
                    self.IO.SendMorse(morse)
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
        self.IO = IO_Delegate.IO_Delegate()
        self.M = Morse.Morse()
    
    def run(self):
        while self.running:
            # Check for messages
            inMorse = self.IO.ReceiveMorse()
            if inMorse != None:
                # print Peer information and message received time
                ct = datetime.today().time()
                msg = self.M.MorseToText(inMorse)
                print(str.format("{0}: {1}\n= {2}", ct, inMorse, msg))
            time.sleep(0.1)       
    
    def kill(self):
        self.running = 0
        
def Program(self):
    
    # Clear screen
    os.system("clear")
    
    # Draw menu
    CLI.UI().DrawMainMenu()
    
    # print(str.format("Active Threads: {0}", threading.active_count())) # trace
        
    # Setup message retrieve thread
    #getMessages = ReceiveThread()
    #getMessages.start()
    
    # Test message for receive thread TRACE
    io = IO_Delegate.IO_Delegate()
    m = Morse.Morse()
    #io.SendMorse(m.TextToMorse("Hello"))
    print(m.TextToMorse("Hello"))
    a = io.RawToMorse('10101010001000101110101000101110101000111011101110')
    print('10101010001000101110101000101110101000111011101110')
    print(a)
    quit() # trace
    # Setup input thread
    #userInput = InputThread()
    #userInput.start()
    
    # print(str.format("Active Threads: {0}", threading.active_count())) # trace
    
    # have parent thread loop until time to kill
    running = True
    while running:
        time.sleep(5) # no need to tie up cpu resources
        pass
        
    getMessages.kill()
    userInput.kill()
        
    # Exit on disconnect
    quit()

# Start program
if __name__ == "__main__":
    Program(None) 
    
    
    
    
    