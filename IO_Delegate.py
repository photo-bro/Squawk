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

#import pdb #debug


class IO_Delegate(object):
    """
    Class containing  methods to transmit and receive morse code messages 
    using a PiFaceDigitalIO board
    """

    def __init__(self, count = .5, channel_out = 7, channel_in = 0):
        """
        Description: Construct IO_Delegate object
        count (float): length in seconds for one dot
        channel_out (int): channel on PiFaceDigitalIO board for outputting morse
        channel_in (int): channel on PiFaceDigitalIO board for incoming morse
        """
        # class variables         
        self.count = count      # in seconds
        self.channel_out = channel_out  
        self.channel_in = channel_in
    
    def Setup(self):
        """
        Description: Initialize PiFaceDigitalIO. Can be called without 
            creating an object. Should be called before attempts to 
            output or receive data. Should only be called once
        """
        pfio.init()
        pfio.digital_write(self.channel_out, 1)
    
    def Cleanup(self):
        """
        Destructor
        Should be called before program termination
        """
        pfio.deinit()
        
    # Best if run on separate thread 
    def SendMorse(self, msg):
        """
        Description: Transmit Morse message over channel_out
        msg (string): Morse code message to be transmitted. Should on contain:
            ' ', '•', or '-'
        An EOT morse char ('• • • - • -') is appended before transmission. 
        NOTE: a prefix message of '• • •' is added due to issues with the first few 
        dots/dashes being corrupted.
        """
        
        # add space to beginning of message to ensure data goes through
        # add  end transmission char to message
#        msg = '• • •' + msg + '• • • - • -' 
        msg += '• • • - • -'
        for c in msg:
            if c == '•':  # On for 1 count
                pfio.digital_write(self.channel_out, 0)
                time.sleep(1 * self.count)
            elif c == '-':  # On for 3 count
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
        """
        Description: Receive morse code message from channel_in. Function 
            checks if EOT has been transmitted. If message contains EOT the 
            morse message is returned without the EOT char. Else None is
            returned.
        Returns: (string) morse message or None if garage
        """
        raw = self._GetRawMessage2()
        m = self._RawToMorse(raw)
        # check if valid message (check EOT char)
        if m[-11:] == '• • • - • -':
            return m[:-11] # return without EOT char
        else:
            return None
    
    def _GetRawMessage(self):
        """
        DEPRECATED
        REQUIRES ReceiveMorse() TO BE UPDATED TO REUSE
        Private Function
        Description: On edge trigger, reads the value of channel_in one time every
            count seconds and adds that value to a buffer. End of message is 
            determined when 10 counts of low ('0') have been consecutively read.
            Beginning of message should contain 6 garage values used to stabilize
            output stream. Low is recorded as '0' and high as '1'
        Return: (string) buffer of values on channel_in once edge triggered. First
            six (6) items and last ten (10) items have been removed before return.
        """
        receiving = True
        s = ''
        # Start at edge trigger
        while pfio.digital_read(self.channel_in) == 1:
            pfio.digital_read(self.channel_in)
            
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
    
    def _GetRawMessage2(self):
        """
        Private Function
        Description: On initial edge trigger, measures how many counts channel_in 
            is high or low
        Return: (string) buffer of values (low = '0', high = '1') from channel_in 
            once edge triggered. 
        """
        s = ''
        dur = 0
        # Start at edge trigger
        while pfio.digital_read(self.channel_in) == 1:
            pfio.digital_read(self.channel_in)
        
        # set current state
        state = 0
        
        # Start high timer
        hiTimeStart = time.time()

        while (dur < 10 * self.count):
            start = time.time()
            if state == 0: # state is high
                # edge trigger to low
                eT = time.time()
                while pfio.digital_read(self.channel_in) == 0:
                     pfio.digital_read(self.channel_in)
                     if (time.time() - eT > 10 * self.count):
                        break
                # Start low timer, end high timer
                lowTimeStart = hiTimeEnd = time.time()
                # Switch state
                state = 1
                # Add values
                for i in range(round((hiTimeEnd - hiTimeStart) / self.count)):
                    s += '1'
            else:
                # edge trigger to hi
                eT = time.time()
                while pfio.digital_read(self.channel_in) == 1:
                     pfio.digital_read(self.channel_in)
                     if (time.time() - eT > 10 * self.count):
                        break
                # Start high timer, end low timer
                hiTimeStart = lowTimeEnd = time.time()
                # Switch state
                state = 0
                # Add values
                for i in range(round((lowTimeEnd - lowTimeStart) / self.count)):
                    s += '0'
            # exit if too long pause
            dur = time.time() - start
        # remove last 10 items (excess zeros) and return
        return s[-10] 
        
    # Parse raw values from input into properly formatted morse code
    def _RawToMorse(self, raw):
        """
        Private Function
        Description: Parse return from _GetRawMessage into proper morse code:
            Grammar:
            '1'       = '•'
            '111'     = '-'
            '0'       = ' '
        raw (string): string containing on the chars '0' and '1'
        Return: (string) containing the proper morse code message from 
            _GetRawMessage.
        """
        m = ''      
        i = 0
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
                    m += '-'
                    i += 3 # consume three spots
                else:
                    m += '•'
                    i += 1 # consume spot2
        return m
                