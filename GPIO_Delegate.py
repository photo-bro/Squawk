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
#  GPIO_Delegate.py                               #
#                                                 #
#  Course: CSCI 333 Networking                    #
#  Professor: John Broere                         #
#  Author: Josh Harmon                            #
#  Created: 4/15/15                               #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
###################################################

# RPi IMPORT WILL ONLY WORK ON RASPBERRY PI
import RPi.GPIO as GPIO
import time, os
import Morse

#import pdb #debug

class GPIO_Delegate(object):


    def __init__(self, channel_out = 11, channel_in = 12, count = .1):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel_out, GPIO.OUT, 0)
        GPIO.setup(channel_in, GPIO.IN)
        GPIO.setwarnings(True)      # for debug
        
        self.count = count      # in seconds
        self.channel_out = channel_out  
        self.channel_in = channel_in
        pass
    
    # Best if run on separate thread 
    def SendMorse(self, msg):
        print(msg)  #trace
        #msg += '@' # add end transmission char to message
        #pdb.set_trace()
        try:
            for c in msg:
                if c == '•':  # On for 1 count
                    GPIO.output(self.channel_out, True)
                    time.sleep(1 * self.count)
                elif c == '−':  # On for 3 count
                    GPIO.output(self.channel_out, True)
                    time.sleep(3 * self.count)
                elif c == ' ':  # On for 1 count
                    time.sleep(1 * self.count)
                else:
                    pass
                GPIO.output(self.channel_out, False)
        finally:
            GPIO.cleanup()  # clean up before exiting


    # Check if dot or dash
    # Build char (series of dot/dosh) until word break
    # Build word until space ' ' is found
    # Build message until '@' char is found
    def ReceiveMorse(self):
        c = ''      # current char received
        s = ''      # current message
        while c != '@': # @ is end char
            s += c               # add current char to message
            c = self.GetChar()   # get next char
        GPIO.cleanup()  # clean up before exiting
        return s
    
    def GetChar(self):
        c = ''      # current char being received
        d = ''      # current dot / dash
        while d != ' ':
            c += d                   # add dot/dash to current char
            d = self.GetDotOrDash()  # get next dot/dash/word break
        return c
        
    def GetDotOrDash(self):
        # Setup channel
        GPIO.setup(channel_in, GPIO.IN)
        # loop until signal comes in
        while GPIO.input(self.channel_in) == False:
            GPIO.input(self.channel_in)
            time.sleep(self.count / 10)    # delay loop slightly
        Start = time.time()                # beginning of dot/dash
        # loop until signal ends
        while GPIO.input(self.channel_in) == True:      
            GPIO.input(self.channel_in)
            time.sleep(self.count / 10)    # delay loop slightly
        End = time.time()                  # end of dot/dash
        # duration of signal in seconds
        Dur = End - Start
        # convert duration to ct
        ct = Dur / self.count
        # check if dot, dash, or word break based on count
        if ct >= 0 and ct < 3:
            return '•'
        elif ct >= 3 and ct < 7:
            return '-'
        elif ct >= 7:
            return ' '
             
        
        
        