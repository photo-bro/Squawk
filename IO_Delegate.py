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

# RPi and PFIO IMPORTS WILL ONLY WORK ON RASPBERRY PI
import RPi.GPIO as GPIO
import pifacedigitalio as pfio

import time, os
import Morse

import pdb #debug

class IO_Delegate(object):

    def __init__(self, mode = "pf", channel_out = 7, channel_in = 0, count = .1):
        # setup proper io system
        if mode == "gp":
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(channel_out, GPIO.OUT, 0)
            GPIO.setup(channel_in, GPIO.IN)
            GPIO.setwarnings(True)      # for debug
            self.mode = "gp"
        elif mode == "pf":
            pfio.init()
            self.mode = "pf"
    
        # class variables         
        self.count = count      # in seconds
        self.channel_out = channel_out  
        self.channel_in = channel_in
    
        # Make sure output is low
        GPIO.output(self.channel_out, False) if (self.mode == "gp") else pfio.digital_write(self.channel_out, 1)
    
    
    # Best if run on separate thread 
    def SendMorse(self, msg):
        # Make sure output is low
        #GPIO.output(self.channel_out, False) if (self.mode == "gp") else pfio.digital_write(self.channel_out, 1)
       
        msg += '• − − • − •' # add '@' (in morse), end transmission char to message
        #pdb.set_trace()
        try:
            for c in msg:
                if c == '•':  # On for 1 count
                    GPIO.output(self.channel_out, True) if (self.mode == "gp") else pfio.digital_write(self.channel_out, 0)
                    time.sleep(1 * self.count)
                elif c == '−':  # On for 3 count
                    GPIO.output(self.channel_out, True) if (self.mode == "gp") else pfio.digital_write(self.channel_out, 0)
                    time.sleep(3 * self.count)
                elif c == ' ':  # 1 count for space
                    time.sleep(7 * self.count)
                else:
                    pass
                GPIO.output(self.channel_out, False) if (self.mode == "gp") else pfio.digital_write(self.channel_out, 1)
        finally:
            # Make sure output is low
            GPIO.output(self.channel_out, False) if (self.mode == "gp") else pfio.digital_write(self.channel_out, 1)

            if (self.mode == "gp"):
                GPIO.cleanup()  # clean up before exiting


    # Check if dot or dash
    # Build char (series of dot/dash) until word break
    # Build word until space ' ' is found
    # Build message until '@' char is found
    def xReceiveMorse(self):
        #pdb.set_trace()
        c = ''      # current char received
        s = ''      # current message
        run = True
        while run: 
            s += c                 # add current char to message
            c = self.__GetChar()   # get next char
            if c == '• − − • − •': # @ is end char
                run = False
            print(c)  #trace
        if self.mode == "gp" :
            GPIO.cleanup()  # clean up before exiting
        return s
    
    def ReceiveMorse(self):
        raw = self.__PF_GetRawMessage()
        print(str.format("Raw: {0}",raw)) #trace
        m = self.RawToMorse(raw)
        return m
    
    def __GetChar(self):
        c = ''      # current char being received
        d = ''      # current dot / dash
        while d != ' ':
            c += d                   # add dot/dash to current char
            if (self.mode == "gp"):
                d = self.__GP_GetDotOrDash()  # get next dot/dash/word break
            else:
                d = self.__PF_GetDotOrDash()
            print(d)  #trace
        # Add spaces between dots and dashes. Ignore before and after first/last dot/dash
        ch = ''
        for i, x in enumerate(c):
            if i == len(c):
                break;
            ch += c[i] + ' '
        return ch
    
    def __GetMorse(self):
        s = ''
        d = ''
        while d != chr(0x17):  # 0x17 is EOT char in UTF-8
            s += d
            d = self.__PF_GetDotOrDash()
            print(d) #trace
        return s
    
    def __PF_GetRawMessage(self):
        receiving = True
        s = ''
        # Start at edge trigger
        while pfio.digital_read(self.channel_in) == 1:
            pfio.digital_read(self.channel_in)
            time.sleep(self.count / 10)    # delay loop slightly
            
        # Check every count if hi or low
        while receiving:
            # Write state to string
            if pfio.digital_read(self.channel_in) == 1:
                s += '0'
            else:
                s += '1'
            #print(pfio.digital_read(self.channel_in)) # trace
            # exit if last 10 counts l
            if s[-10:] == "0000000000":
                receiving = False
            time.sleep(self.count)  # sleep rest of count
        # remove last 10 items and return
        return s[:-10] 
    
    
    # Parse raw values from input into properly formatted morse code
    def RawToMorse(self, raw):
        m = ''
        i = 0
        # '1'       = '•'
        # '111'     = '−'
        # '0'       = ' '
        # '000'     = '   '
        # '0000000' = '       ' 
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
#                    print(str.format("{0}, {1}: {2}", i, '111', '−'))  # trace
                    i += 3 # consume two spots
                    # Check for following zero
#                    if (i+1) < len(raw) and raw[i+1] == '0':
#                        i += 1 # consume following 0
                else:
                    m += '•'
                    i += 1
#                    print(str.format("{0}, {1}: {2}", i, raw[i], '•'))  # trace
#                    if (i+1) < len(raw) and raw[i+1] == '0':
#                        i += 1 # consume following 0
#                m += ' '   # space between blips in char
#            else:# raw[i] == '0':
#                m += ' '
#                print(str.format("{0}, {1}: {2}", i, raw[i], '\' \''))  # trace
                # '000'
#                if ((i+2) < len(raw) and # check if in bounds
#                     raw[i+1] == '0' and raw[i+2] == '0'):
#                    m += '  '  # add 2 spaces (assuming one already added) between char in word
#                    print(str.format("{0}, {1}: {2}", i, v, '\'   \''))  # trace
#                    i += 2     # consume the two spaces
#                    # '0000000'
#                    if ((i+4) < len(raw) and # check if in bounds 
#                        raw[i+1] == '0'  and raw[i+2] == '0' and   
#                        raw[i+3] == '0'  and raw[i+4] == '0'
#                        ):
#                        m += '    '  # add 4 more spaces (7 total) between words
#                        print(str.format("{0}, {1}: {2}", i, v, '\'       \''))  # trace
#                        i += 4       # consume the seven spaces
            
            


#        for w in raw.split('0000000'):
#            # split into chars
#            for c in w.split('000'):
#                # split into blips
#                for i in range(len(c)):
#                    if c[i] == '1':
#                        if (i+2) < len(c) and c[i+1] == '1' and c[i+2] == '1':
#                            m += '−'
#                            # one space between each blip in a char
#                            # unless at end of char
##                            if (i+5) < len(c) and c[i+5] != '0':
##                                m += ' ' # one space between each blip in a char
#                            i += 2   # skip over next 2 blips
#                            continue
#                        m += '•'
#                        # one space between each blip in a char
#                        # unless at end of char
##                        if (i+3) < len(c) and c[i+3] != '0':
##                            m += ' '                              
#                m += '  '  # three spaces between chars
#            m += '       ' # seven spaces between words
        return m
        
    
    def __PF_GetDotOrDash(self):
        # loop until signal comes in
        while pfio.digital_read(self.channel_in) == 1:
            pfio.digital_read(self.channel_in)
            time.sleep(self.count / 10)    # delay loop slightly
        Start = time.time()                # beginning of dot/dash
        # loop until signal ends
        while pfio.digital_read(self.channel_in) == 0:      
            pfio.digital_read(self.channel_in)
            time.sleep(self.count / 10)    # delay loop slightly
        End = time.time()                  # end of dot/dash
        # duration of signal in seconds
        Dur = End - Start
        # convert duration to counts
        ct = Dur / self.count
        # check if dot, dash, or word break based on count
        if ct >= 0 and ct < 3:
            return '• '
        elif ct >= 3 and ct < 7:
            return '- '
        elif ct >= 7 and ct < 10:
            return ' '
        elif ct >= 10:      # end transmission
            return chr(0x17)
        
    def __GP_GetDotOrDash(self):
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
             
        
        
        