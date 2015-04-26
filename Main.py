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
    def __init__(self, count = .5):
        threading.Thread.__init__(self)
        self.running = 1
        self.IO = IO_Delegate.IO_Delegate(count)
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
                    print(str.format("Sending message: {0} => {1}", outMessage, morse))
                    self.IO.SendMorse(morse)
                    print("Sent.")
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
    def __init__(self, count = .5):
        threading.Thread.__init__(self)
        self.running = 1
        self.IO = IO_Delegate.IO_Delegate(count)
        self.M = Morse.Morse()
    
    def run(self):
        while self.running:
            # Check for messages
            inMorse = self.IO.ReceiveMorse()
            if inMorse != None:
                ct = datetime.today().time()
                msg = self.M.MorseToText(inMorse)
                print(str.format("\nReceived Message at {0}:{1}:{2} : {3} \nMessage: {4}", 
                                 ct.hour, ct.minute, ct.second, inMorse, msg.upper()))
                sys.stdout.flush()
            time.sleep(0.1)       
    
    def kill(self):
        self.running = 0
        
def Program(self):
    
    # Clear screen
    os.system("clear")
    
    # Draw menu
    CLI.UI().DrawMainMenu()
    
    # Request count length
    count = input("Count Length: ")
    
    # Init IO
    IO_Delegate.IO_Delegate().Setup()
            
    # Setup message retrieve thread
    getMessages = ReceiveThread(float(count))
    getMessages.start()
    
    # Setup input thread
    userInput = InputThread(float(count))
    userInput.start()
        
    # have parent thread loop until time to kill
    running = True
    while running:
        time.sleep(5) # no need to tie up cpu resources
        pass
        
    # kill threads    
    getMessages.kill()
    userInput.kill()
        
    # Cleanup IO
    IO_Delegate.IO_Delegate().Cleanup()
    
    # Exit
    quit()

# Start program
if __name__ == "__main__":
    Program(None) 
    
    
    
    
    