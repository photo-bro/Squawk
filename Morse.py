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
#  Morse.py                                       #
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

class Morse(object):
    """
    Class containing methods to convert plain text to and from morse code
    Morse code class symbology:
    Name  Symbol  Counts     Value
    -------------------------------
    Dot:   '•'    1 count     HIGH
    Dash:  '-'    3 counts    HIGH
    Space: ' '    1 count     LOW
    -------------------------------
        Space between each components of a character is one (1) count. The 
    space between each character is three (3) counts. The space between
    each word is seven (7) counts.
    Credit:
    http://morsecode.scphillips.com/morse2.html
    """
    
    def __init__(self):
        """
        Constructor
        """
        self.MorseDict = {'a':'• -',     
                          'b':'- • • •',    
                          'c':'- • - •',    
                          'd':'- • •',    
                          'e':'•',    
                          'f':'• • - •',    
                          'g':'- - •',    
                          'h':'• • • •',    
                          'i':'• •',    
                          'j':'• - - -',    
                          'k':'- • -',    
                          'l':'• - • •',    
                          'm':'- -',
                          'n':'- •',    
                          'o':'- - -',    
                          'p':'• - - •',    
                          'q':'- - • -',    
                          'r':'• - •',   
                          's':'• • •',   
                          't':'-',    
                          'u':'• • -',    
                          'v':'• • • -',    
                          'w':'• - -',    
                          'x':'- • • -',    
                          'y':'- • - -',    
                          'z':'- - • •',    
                          '0':'- - - - -',    
                          '1':'• - - - -',    
                          '2':'• • - - -',    
                          '3':'• • • - -',    
                          '4':'• • • • -',    
                          '5':'• • • • •',    
                          '6':'- • • • •',   
                          '7':'- - • • •',   
                          '8':'- - - • •',    
                          '9':'- - - - •',
                          '.':'• - • - • -',    
                          ',':'- - • • - -',   
                          ':':'- - - • • •',    
                          '?':'• • - - • •',    
                          '\'':'• - - - - •',    
                          '-':'- • • • • -',    
                          '/':'- • • - •',    
                          '(':'- • - - • -',    
                          '\"':'• - • • - •',   
                          '@':'• - - • - •',    
                          '=':'- • • • -'}

    
    def TextToMorse(self, text):
        """
        Description: Convert 'text' into properly formatted morse code string
        text (string): plain text string of characters
        Return: (string) properly formatted morse code string. See class constructor
            for specifics about symbology
        """
        s = '' 
        # split message into words         
        for w in text.split():
            # convert each char in each word
            for c in w.lower():
                try:
                    s += self.MorseDict[c]
                    s += '   '  # 3 spaces between characters in a word
                except:
                    # invalid letter, assume blank
                    pass
            # 7 spaces (each space is 1 count) between words
            s += '    ' 
        return s
    
    
    def MorseToText(self, msg):
        """
        Description: Convert properly formatted morse code string into plain text.
        msg (string): properly formatted morse code string
        Return: (string) translated plain text string
        """
        s = ''
        # Split message into groups of individual words
        for w in msg.split('       '):  # 7 spaces between words
            # Split word into groups of individual chars
            for c in w.split('   '):    # 3 spaces between chars
                s += self.__MorseCharToText(c)    
            s += ' ' # space between words
        return s    
    

    def __MorseCharToText(self, char):
        """
        Private Function
        Description: Reverse search dictionary to find plain text char from
            morse code char.
        char (string): morse code character
        Return: (chr) translated plain text character
        """
        # Find key from value in dictionary
        # Dictionary might not be the best data structure for this.... oh whale
        key = [k for k, v in self.MorseDict.items() if v == char]
        if key:
            return key[0]
        else:
            return ''