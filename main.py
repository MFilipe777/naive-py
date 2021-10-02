import asyncio
import websockets
import json
from flask import Flask, request
from flask.json import jsonify
import json
from blockchain import *
from p2p import *

def http_server(http_port, server : Node):
    app = Flask(__name__)
    
    @app.route("/blocks", methods = ["GET"])
    def get_blocks():
        return get_serialized_blockchain()
    
    @app.route("/mine_block", methods = ["POST"])
    def mine():
        new_block = generate_next_block(request.form["data"])
        return get_serialized_block(new_block)
    
    @app.route("/peers", methods = ["GET"])
    def get_peers():
        return  get_sockets()
    
    @app.route("/add_peer")
    def add_peer():
        host, port = list(map(int, request.json.peer.split(":")))
        server.connect_with_node(host, port, reconnect=True)

    app.run()

if __name__ == "__main__":
    p2p = Node("0.0.0.0",5431)
    http = http_server("0.0.0.0", 4852)