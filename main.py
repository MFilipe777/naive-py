from flask import Flask, request
from flask.json import jsonify
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
        return  jsonify(get_sockets())
    
    @app.route("/add_peer", methods = ["POST"])
    def add_peer():
        host, port = request.form["host"], request.form["port"]
        server.connect_with_node(host, port, reconnect=True)

    app.run()

if __name__ == "__main__":
    p2p = Node("0.0.0.0",5431)
    http = http_server("0.0.0.0", 4852)