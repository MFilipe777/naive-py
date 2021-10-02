import asyncio
import websockets
from enum import Enum
from node import Node
from blockchain import *

sockets = []

class Message_Type(Enum):
    QUERY_LATEST = 0
    QUERY_ALL = 1
    RESPONSE_BLOCKCHAIN = 2

class Message:
    def __init__(self):
        self.type = Message_Type()
        self.data = None

def init_p2p_server():
    def __init__(self, p2p_port, p2p_host):
        server = Node(p2p_host, p2p_port)
        server.init_server()
        print("Listening websocket p2p port on:", p2p_port)

def get_sockets():
    return sockets