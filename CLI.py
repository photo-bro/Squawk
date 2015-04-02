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
#  CLI.py                                         #
#                                                 #
#  Course: CSCI 333 Networking                    #
#  Professor: John Broere                         #
#  Author: Josh Harmon                            #
#  Created: 3/5/15                                #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
###################################################

# Local imports
import Network_Delegate  # for Peer class
import Log

class UI():
    
    
    def PeerInfoPrompt(self):
        peer_location = input("Peer location: ")
        # Exit program
        if peer_location == "quit":
            quit()
        peer_port = input("Peer port: ")
        return Network_Delegate.Peer(peer_location, peer_port) 
    
    def DrawMainMenu(self):
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║    ███████╗ ██████╗ ██╗   ██╗ █████╗ ██╗    ██╗██╗  ██╗           ║")
        print("║    ██╔════╝██╔═══██╗██║   ██║██╔══██╗██║    ██║██║ ██╔╝           ║")
        print("║    ███████╗██║   ██║██║   ██║███████║██║ █╗ ██║█████╔╝            ║")
        print("║    ╚════██║██║▄▄ ██║██║   ██║██╔══██║██║███╗██║██╔═██╗            ║")
        print("║    ███████║╚██████╔╝╚██████╔╝██║  ██║╚███╔███╔╝██║  ██╗           ║")
        print("║    ╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝           ║")
        print("║                                                                   ║")
        print("║     \"A simple socket based peer to peer chat client\"              ║")
        print("║                                                                   ║")
        print("║     Created by Josh Harmon                                        ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")
    