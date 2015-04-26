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
#  IO_Delegate.py                                 #
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

# PFIO IMPORT WILL ONLY WORK ON RASPBERRY PI
import pifacedigitalio as pfio

import time, os
import Morse

import pdb #debug




class IO_Delegate(object):

    def __init__(self, count = .5, channel_out = 7, channel_in = 0):
        # setup proper io system
        #pfio.init()
    
        # class variables         
        self.count = count      # in seconds
        self.channel_out = channel_out  
        self.channel_in = channel_in
    
        # Make sure output is low
        #pfio.digital_write(self.channel_out, 1)
    
    def Setup(self):
        #   Not in constructor because it only needs to be called from the 
        # first instance
        pfio.init()
        pfio.digital_write(self.channel_out, 1)
    
    def Cleanup(self):
        pfio.deinit()
        
    # Best if run on separate thread 
    def SendMorse(self, msg):
        # Make sure output is low
        #pfio.digital_write(self.channel_out, 1)
       
        # add space to beginning of message to ensure data goes through
        # add  end transmission char to message
        msg = '• • •' + msg + '• • • − • −' 
        for c in msg:
            if c == '•':  # On for 1 count
                pfio.digital_write(self.channel_out, 0)
                time.sleep(1 * self.count)
            elif c == '−':  # On for 3 count
                pfio.digital_write(self.channel_out, 0)
                time.sleep(3 * self.count)
            elif c == ' ':  # 1 count for space
                time.sleep(1 * self.count)
            else:
                pass
            # set low at end of each loop
            pfio.digital_write(self.channel_out, 1)
            
        # set low before exit
        pfio.digital_write(self.channel_out, 1)
    
    def ReceiveMorse(self):
        raw = self._GetRawMessage()
        m = self._RawToMorse(raw)
        # check if valid message (check EOT char)
        if m[-11:] == '• • • − • −':
            return m[:-11] # return without EOT char
        else:
            return None
    
    def _GetRawMessage(self):
        receiving = True
        s = ''
        # Start at edge trigger
        while pfio.digital_read(self.channel_in) == 1:
            pfio.digital_read(self.channel_in)
            #time.sleep(self.count / 10)    # delay loop slightly
            
        # Check every count if hi or low
        while receiving:
            # Write state to string
            if pfio.digital_read(self.channel_in) == 0:
                s += '1'
            else:
                s += '0'

            # exit if last 10 counts l
            if s[-10:] == "0000000000":
                receiving = False
                break
            
            time.sleep(self.count)  # sleep rest of count
        # remove last 10 items and return
        return s[6:-10] 
    
    # Parse raw values from input into properly formatted morse code
    def _RawToMorse(self, raw):
        m = ''
        i = 0
        # '1'       = '•'
        # '111'     = '−'
        # '0'       = ' '
        while i < len(raw):
            if raw[i] == '0':
                m += ' '
                i += 1
                continue
            # '1'
            if raw[i] == '1':
                # '111'
                if ((i+2) < len(raw) and # check if in bounds
                     raw[i+1] == '1' and raw[i+2] == '1'):
                    m += '−'
                    i += 3 # consume three spots
                else:
                    m += '•'
                    i += 1 # consume spot2
        return m
                