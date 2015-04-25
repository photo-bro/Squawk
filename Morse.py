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

    def __init__(self):
        self.MorseDict = {'a':'• −',     
                          'b':'− • • •',    
                          'c':'− • − •',    
                          'd':'− • •',    
                          'e':'•',    
                          'f':'• • − •',    
                          'g':'− − •',    
                          'h':'• • • •',    
                          'i':'• •',    
                          'j':'• − − −',    
                          'k':'− • −',    
                          'l':'• − • •',    
                          'm':'− −',
                          'n':'− •',    
                          'o':'− − −',    
                          'p':'• − − •',    
                          'q':'− − • −',    
                          'r':'• − •',   
                          's':'• • •',   
                          't':'−',    
                          'u':'• • −',    
                          'v':'• • • −',    
                          'w':'• − −',    
                          'x':'− • • −',    
                          'y':'− • − −',    
                          'z':'− − • •',    
                          '0':'− − − − −',    
                          '1':'• − − − −',    
                          '2':'• • − − −',    
                          '3':'• • • − −',    
                          '4':'• • • • −',    
                          '5':'• • • • •',    
                          '6':'− • • • •',   
                          '7':'− − • • •',   
                          '8':'− − − • •',    
                          '9':'− − − − •',
                          '.':'• − • − • −',    
                          ',':'− − • • − −',   
                          ':':'− − − • • •',    
                          '?':'• • − − • •',    
                          '\'':'• − − − − •',    
                          '-':'− • • • • −',    
                          '/':'− • • − •',    
                          '(':'− • − − • −',    
                          '\"':'• − • • − •',   
                          '@':'• − − • − •',    
                          '=':'− • • • −'}

    
    def TextToMorse(self, text):
        s = '' 
        # split message into words         
        for w in text.split():
            # convert each char in each word
            for c in w.lower():
                try:
                    s += self.MorseDict[c]
                    s += '   '  # 3 spaces between characters in a word
                except e:
                    # invalid letter, assume blank
                    pass
            # 7 spaces (each space is 1 count) between words
            s += '       ' 
        return s
    
    
    def MorseToText(self, msg):
        s = ''
        # Split message into groups of individual words
        for w in msg.split("       "):  # 7 spaces between words
            # Split word into groups of individual chars
            for c in w.split("   "):    # 3 spaces between chars
                s += self.__MorseCharToText(c)    
        return s    
    

    def __MorseCharToText(self, char):
        # Find key from value in dictionary
        # Dictionary might not be the best data structure for this.... oh whale
        for k, v in self.MorseDict.items():
            if char == v:
                return k
            else:
                return ""