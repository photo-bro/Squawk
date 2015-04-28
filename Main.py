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
import IO_Delegate
import Morse

#import pdb #debug

class Graphics():
    """
    Class containing menus to be printed and color codes
    """
    def DrawMainMenu(self):
        print("╔═══════════════════════════════════════════════════════════════════════════════════════════════╗")
        print("║                  ███████╗ ██████╗ ██╗   ██╗ █████╗ ██╗    ██╗██╗  ██╗                         ║")
        print("║                  ██╔════╝██╔═══██╗██║   ██║██╔══██╗██║    ██║██║ ██╔╝                         ║")
        print("║                  ███████╗██║   ██║██║   ██║███████║██║ █╗ ██║█████╔╝                          ║")
        print("║                  ╚════██║██║▄▄ ██║██║   ██║██╔══██║██║███╗██║██╔═██╗                          ║")
        print("║                  ███████║╚██████╔╝╚██████╔╝██║  ██║╚███╔███╔╝██║  ██╗                         ║")
        print("║                  ╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝                         ║")
        print("║                                                                                               ║")
        print("║                     \"A morse code based peer to peer chat client\"                             ║")
        print("║                                                                                               ║")
        print("║                       Created by Josh Harmon                                                  ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════════════════════╝")
    
    def DrawInstructions(self):
        print("██╗███╗   ██╗███████╗████████╗██████╗ ██╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗")
        print("██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝██╗")
        print("██║██╔██╗ ██║███████╗   ██║   ██████╔╝██║   ██║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗╚═╝")
        print("██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║   ██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║██╗")
        print("██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║╚═╝")
        print("╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ")
        print("Count Length: The number of seconds a dot (•) is held for. Values smaller than .05 do not ")
        print("always work and behave unpredictably")
        print("To exit, type \'quit\'")
        print("═══════════════════════════════════════════════════════════════════════════════════════════════")

    # http://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
    class color:
        PURPLE    = '\033[95m'
        CYAN      = '\033[96m'
        DARKCYAN  = '\033[36m'
        BLUE      = '\033[94m'
        GREEN     = '\033[92m'
        YELLOW    = '\033[93m'
        RED       = '\033[91m'
        BOLD      = '\033[1m'
        UNDERLINE = '\033[4m'
        END       = '\033[0m'

class InputThread(threading.Thread):
    """
    Class for creating separate thread for user input to prevent blocking
    Concept and code credit:
    http://code.activestate.com/recipes/578591-primitive-peer-to-peer-chat/
    """
    def __init__(self, count = .5):
        """
        Constructor
        count (float): length in seconds for one dot. Has to be same for all devices
        """
        threading.Thread.__init__(self)
        self.running = 1
        self.IO = IO_Delegate.IO_Delegate(count)
        self.M = Morse.Morse()
    
    def run(self):
        """
        Description: User input loop. Prompt user for message and attempt
            transmit message. "quit" will quit entire program
        """
        while self.running:
            outMessage =  input("")
            if outMessage:       
                # easy exit    
                if outMessage == "quit":
                    os._exit(1)                
                # Don't send empty message
                try:
                    #pdb.set_trace()
                    morse = self.M.TextToMorse(outMessage)
                    print(str.format("{2}Sending message: {0} => {1}{3}", outMessage, morse, 
                                     Graphics.color.BOLD, Graphics.color.END))
                    self.IO.SendMorse(morse)
                    print(str.format("{0}Sent.{1}", Graphics.color.BOLD, Graphics.color.END))
                except:
                    Exception
            time.sleep(0.5)
                
    def kill(self):
        """
        Destroy thread
        """
        self.running = 0

class ReceiveThread(threading.Thread):
    """
    Class for creating separate thread for printing incoming messages
    Concept and code credit:
    http://code.activestate.com/recipes/578591-primitive-peer-to-peer-chat/
    """
    def __init__(self, count = .5):
        """
        Constructor
        count (float): length in seconds for one dot. Has to be same for all devices
        """
        threading.Thread.__init__(self)
        self.running = 1
        self.IO = IO_Delegate.IO_Delegate(count)
        self.M = Morse.Morse()
    
    def run(self):
        """
        Description: Loop and check for incoming message. Read message once input is 
            detected. Print message to screen
        """
        while self.running:
            # Check for messages
            inMorse = self.IO.ReceiveMorse()
            if inMorse != None:
                ct = datetime.today().time()
                msg = self.M.MorseToText(inMorse)
                print(Graphics.color.BOLD)
                print(str.format("\nReceived Message at {0}:{1}:{2} : {3} \nMessage: {4}", 
                                 ct.hour, ct.minute, ct.second, inMorse, msg.upper()))
                print(Graphics.color.END)
                sys.stdout.flush()
            time.sleep(0.5)       
    
    def kill(self):
        """
        Destroy thread
        """
        self.running = 0
        
def Program(self):
    """
    Program entry
    Head of execution
    """
    
    # Clear screen
    os.system("clear")
    
    # Draw menu and instructions
    print(Graphics.color.RED)
    Graphics.DrawMainMenu(self)
    print(Graphics.color.BLUE)
    Graphics.DrawInstructions(self)
    print(Graphics.color.END)
    
    # Request count length
    count = input(str.format("{0}Count Length (in seconds):{1} ", Graphics.color.BOLD, Graphics.color.END))
    # horrible loop for data validation
    # couldn't think of a better solution at the moment
    while True:
        try:
            float(count)
            break
        except:
            count = input(str.format("{0}Count Length (in seconds):{1} ", Graphics.color.BOLD, Graphics.color.END))
        
    # Init IO
    IO_Delegate.IO_Delegate().Setup()
            
    # Setup message receive thread
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
        
    # Kill threads    
    getMessages.kill()
    userInput.kill()
        
    # Cleanup IO
    IO_Delegate.IO_Delegate().Cleanup()
    
    # Exit
    quit()

# Start program
if __name__ == "__main__":
    Program(None) 
    
    
    
    
    
