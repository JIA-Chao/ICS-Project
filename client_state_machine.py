"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
@editted by Jingxian Xu and Jia Zhao
"""
from chat_utils import *
import json

# ------RSA IMPLEMENTATION-------
import RSA
import en_de


class ClientSM:
    def __init__(self, s):
        """s: check chat_client_class, s is socket. """
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

# ------RSA IMPLEMENTATION-------
        self.peer_pubkeys = {}    # peer pubkeys while chatting
        self.prikey = []    # client's prikey
        self.pubkey = []   # client's pubkey

    def set_pri(self, pri):
        self.prikey = pri

    def get_pri(self):
        return self.prikey

    def set_pub(self, pub):
        self.pubkey = pub

    def get_pub(self):
        return self.pubkey
# -------------------------------

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        # cpubkey: pubkey of the client who "c" others
        msg = json.dumps({"action": "connect", "target": peer, "cpubkey": self.pubkey})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'

# ------RSA IMPLEMENTATION-------
            self.peer_pubkeys = response["pubkeys"]
            self.out_msg += 'Peer pubkeys here:' + str(self.peer_pubkeys) + '\n'
            self.out_msg += '-----------------------------------\n'
            return True

        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return False

    def disconnect(self):
        msg = json.dumps({"action": "disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

# ------RSA IMPLEMENTATION-------
        self.peer_pubkeys = {}

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''

        if self.state == S_LOGGEDIN:
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action": "time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action": "list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

# ------RSA IMPLEMENTATION-------
# Search cannot work for RSA
#                 elif my_msg[0] == '?':
#                     term = my_msg[1:].strip()
#                     mysend(self.s, json.dumps({"action": "search", "target": term}))
#                     search_rslt = json.loads(myrecv(self.s))["results"]  # result list
#                     if (len(search_rslt)) > 0:
#                         self.out_msg += str(search_rslt) + '\n\n'
#                     else:
#                         self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "poem", "target": poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    if len(poem) > 0:
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet' + poem_idx + ' not found\n\n'
# --------------MUSIC----------------
                elif my_msg[0] == 'm':
                    mood_l=['tired','not bad','sad']
                    if my_msg[2:] in mood_l:
                        #self.state = S_MUSIC
                        mood=my_msg[2:]
                        mysend(self.s,json.dumps({'action':'music','mood':mood}))
                        self.out_msg += 'your music is coming soon!'
                    else:
                        self.out_msg += "please choose one mood from 'sad','tired','not bad'"
                    


# ------RSA IMPLEMENTATION-------
                elif my_msg == 'k':
                    mysend(self.s, json.dumps({"action": "search_pubkeys"}))
                    all_keys = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "All Public Keys Here: "
                    self.out_msg += str(all_keys)

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err :
                    self.out_msg += " json.loads failed " + str(err)
                    return self.out_msg
            
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += '\n\n' + 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer + '. ' + 'Chat away!\n\n'
# ------RSA IMPLEMENTATION-------
                    # print(self.peer, peer_msg["cpubkey"])
                    self.peer_pubkeys[self.peer] = peer_msg["cpubkey"]  # add peer's pubkey
                    self.out_msg += "Peer Public Keys Here:" + str(self.peer_pubkeys) + '\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING

        elif self.state == S_CHATTING:

#------RSA IMPLEMENTATION-------
# RSA ENCRYPTION AND DECRYPTION PART
            if len(my_msg) > 0:
                en_msg = en_de.encrypt(my_msg)
                for name, pubkey in self.peer_pubkeys.items():
                    rsa_msg = RSA.RSA_encrypt(en_msg, pubkey)
                    # self.out_msg += 'RSA Msg Here:' + str(rsa_msg) + '\n'
                    mysend(self.s, json.dumps({"action": "exchange", "from": "[" + self.me + "]",
                                               "to": name, "message": rsa_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
                    self.peer_pubkeys = {}

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.peer_pubkeys[self.peer] = peer_msg["cpubkey"]
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                    self.peer_pubkeys = {}
                else:
                    # print('Msgs Before RSA Decryption:', peer_msg["message"])
                    prikey = self.get_pri()
                    # print('Your PriKey:', prikey)
                    en_msg = RSA.RSA_decrypt(peer_msg["message"], prikey)
                    # print('Msgs After RSA Decryption:', en_msg)
                    de_msg = en_de.decrypt(en_msg)
                    self.out_msg += peer_msg["from"] + " " + de_msg
# ------------------------------------
                
            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu

        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
