from hashlib import sha256
from time import time 
import json 

class Block:
    def __init__(self, index, hash, previous_hash, timestamp, data, difficulty, nonce):
        self.index = index
        self.hash = hash
        self.previous_hash = previous_hash
    
        self.timestamp = timestamp
        self.data = data

        self.difficulty = difficulty
        self.nonce = nonce

genesis_block = Block(0, "93fb2fe35fdee5dd9363cf3efe72481380e416f4509e8fb67b58758a872f6b63", None, 1465154705, "hi")
blockchain = [genesis_block]

BLOCK_GENERATION_INTERVAL      = 10  # seconds
DIFFICULTY_ADJUSTMENT_INTERVAL = 10  # in blocks

def calculate_hash(index, previous_hash, timestamp, data):
    return sha256(''.join(list(map(str,[index, previous_hash, timestamp, data]))).encode("utf-8")).hexdigest()

def add_block(block):
    blockchain.append(block)

def generate_next_block(data):
    previous_block = get_latest_block()

    next_index = previous_block.index  + 1
    next_timestamp = time()

    next_hash = calculate_hash(next_index, previous_block.hash, next_timestamp, data)

    next_block = Block(next_index, next_hash, previous_block.hash, next_timestamp, data)
    add_block(next_block)
    return next_block

def get_latest_block():
    return blockchain[-1]

def is_valid_new_block(new_block, previous_block):
    if (previous_block.index + 1 != new_block.index):
        print("Invalid index")
        return False
    elif (new_block.previous_hash != previous_block.hash):
        print("Invalid prev. hash")
        return False
    elif (calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.data) != new_block.hash):
        print("Invalid hash")
        return False
    elif not is_valid_block_structure(new_block):
        return False
    
    return True

def is_valid_block_structure(block: Block):
    return type(block.index) == int and type(block.hash) == str and type(block.previous_hash) == str and type(block.timestamp) == str and type(block.data) == str

def is_valid_chain(blockchain):
    if blockchain[0] != genesis_block:
        return False
    return all([is_valid_new_block(blockchain[i], blockchain[i-1]) for i in range(1,len(blockchain))])

def replace_chain(new_blockchain):
    if is_valid_chain(new_blockchain) and len(new_blockchain) > len(get_blockchain()):
        print("Received blockchain is valid. Replacing current blockchain with received blockchain")
        blockchain = new_blockchain
    else:
        print("Received blockchain is invalid")

def get_blockchain():
    return blockchain

def get_serialized_block(block : Block):
    serialized_block = {"index":block.index, "hash": block.hash, "previous hash": block.previous_hash, "timestamp": block.timestamp, "data": block.data}
    return serialized_block

def get_serialized_blockchain():
    serialized_blockchain = list(map(get_serialized_block, blockchain))
    return json.dumps(serialized_blockchain)