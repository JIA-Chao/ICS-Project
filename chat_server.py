"""
Created on Tue Jul 22 00:47:05 2014
@author: alina, zzhang
@edited by Jingxian Xu and Jia Zhao
"""

import time
import socket
import select
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp
import player
import reporter


class Server:
    def __init__(self):
        self.new_clients = []
        self.logged_name2sock = {}
        self.logged_sock2name = {}
        self.all_sockets = []
        self.group = grp.Group()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        self.indices = {}
        self.sonnet = indexer.PIndex("AllSonnets.txt")
        # self.santa_hat =

# ------RSA IMPLEMENTATION--------
        self.rsa_pubkeys = {}   # this dictionary stores all clients' public keys

    def new_client(self, sock):
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:
                if msg["action"] == "login":
                    name = msg["name"]
                    if self.group.is_member(name) != True:
                        self.new_clients.remove(sock)
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        if name not in self.indices.keys():
                            try:
                                self.indices[name] = pkl.load(
                                    open(name + '.idx', 'rb'))
                            except IOError:  # chat index does not exist, then create one
                                self.indices[name] = indexer.Index(name)

# ------RSA IMPLEMENTATION--------
                        self.rsa_pubkeys[name] = msg["pubkey"]   # add new login client's pubkey
                        print('RSA Key Pair Is Successfully Generated!')
                        print(name + ' logged in')
                        self.group.join(name)
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "ok"}))

                    else:
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "duplicate"}))
                        print(name + ' duplicate login attempt')
                else:
                    print('wrong code received')
            else:
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx', 'wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]

# ------RSA IMPLEMENTATION--------
        del self.rsa_pubkeys[name]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

    def handle_msg(self, from_sock):
        msg = myrecv(from_sock)
        if len(msg) > 0:
            msg = json.loads(msg)
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                cpubkey = msg["cpubkey"]
                if to_name == from_name:
                    msg = json.dumps({"action": "connect", "status": "self"})
                    mysend(from_sock, json.dumps(
                        {"action": "connnect", "status": "self"}))
                elif self.group.is_member(to_name):
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)

# ------RSA IMPLEMENTATION-------
                    their_pubk = {}   # this dict stores all others public keys
                    for guy in the_guys[1:]:
                        their_pubk[guy] = self.rsa_pubkeys[guy]
                    mysend(from_sock, json.dumps(
                        {"action": "connect", "status": "success", "pubkeys": their_pubk}))  # send their_pubk to client

                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps(
                            {"action": "connect", "status": "request", "from": from_name, "cpubkey": cpubkey}))
                        # send the client's pubkey to each other in the chatting group

                else:
                    msg = json.dumps(
                        {"action": "connect", "status": "no-user"})
                    mysend(from_sock, msg)

            elif msg["action"] == "exchange":
                """Finding the list of people to send to and index message"""
                to_name = msg["to"]
                to_sock = self.logged_name2sock[to_name]
                messages = msg["message"]

# ------RSA IMPLEMENTATION--------
                print('Here Is What Server Gets:', messages)
                mysend(
                    to_sock, json.dumps({"action": "exchange", "from": msg["from"], "message": messages}))

            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps({"action": "disconnect"}))

            elif msg["action"] == "list":
                "...needs to use self.group functions to work"
                cur_name = self.logged_sock2name[from_sock]
                result = self.group.list_all(cur_name)
                mysend(from_sock, json.dumps(
                    {"action": "list", "results": result}))

            elif msg["action"] == "poem":
                poem_index = int(msg['target'])
                poem = self.sonnet.get_poem(poem_index)
                poem = ' '.join(poem)
                mysend(from_sock, json.dumps(
                    {"action": "poem", "results": poem}))

            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps(
                    {"action": "time", "results": ctime}))
                
# ------MUSIC FUNCTION-------                 
            elif msg['action'] == 'music':
                from_name = self.logged_sock2name[from_sock]
                mood=msg['mood']
                player.run(mood,from_name)

            elif msg['action'] == 'report':
                from_name = self.logged_sock2name[from_sock]
                r=reporter.get_report(from_name)
                mysend(from_sock, json.dumps(
                    {"action": "report", "results": r}))

# ------RSA IMPLEMENTATION-------
# Search cannot work for RSA
#             elif msg["action"] == "search":
#                 term = msg["target"]
#                 from_name = self.logged_sock2name[from_sock]
#                 result1 = self.indices[from_name].search(term)
#                 result = []
#                 for each in result1:
#                     result.append(each[1])
#                 mysend(from_sock, json.dumps(
#                     {"action": "search", "results": result}))


# ------RSA IMPLEMENTATION-------
            elif msg["action"] == "search_pubkeys":
                """let the client know all pubkeys in the chat system. """
                all_pubkeys = self.rsa_pubkeys
                mysend(from_sock, json.dumps(
                    {"action": "search_", "results": all_pubkeys}))

        else:
            # client died unexpectedly
            self.logout(from_sock)

    def run(self):
        print('starting server...')
        while(1):
            read, write, error = select.select(self.all_sockets, [], [])
            print('checking logged clients..')
            for logc in list(self.logged_name2sock.values()):
                if logc in read:
                    self.handle_msg(logc)
            print('checking new clients..')
            for newc in self.new_clients[:]:
                if newc in read:
                    self.login(newc)
            print('checking for new connections..')
            if self.server in read:
                # new client request
                sock, address = self.server.accept()
                self.new_client(sock)


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
