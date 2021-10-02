from blockchain import *
from p2pnetwork.node import Node

sockets = []

def init_p2p_server():
    def __init__(self, p2p_port, p2p_host):
        server = Node(p2p_host, p2p_port)
        server.init_server()
        print("Listening websocket p2p port on:", p2p_port)

def get_sockets():
    return sockets