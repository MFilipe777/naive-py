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


genesis_block = Block(
    0, "93fb2fe35fdee5dd9363cf3efe72481380e416f4509e8fb67b58758a872f6b63", None, 1465154705, "hi", 5, 0)
blockchain = [genesis_block]

BLOCK_GENERATION_INTERVAL = 10  # seconds
DIFFICULTY_ADJUSTMENT_INTERVAL = 10  # in blocks


def calculate_hash(index, previous_hash, timestamp, data, difficulty, nonce):
    return sha256(''.join(list(map(str, [index, previous_hash, timestamp, data, difficulty, nonce]))).encode("utf-8")).hexdigest()


def calculate_hash_for_block(block: Block):
    return sha256(''.join(list(map(str, [block.index, block.previous_hash, block.timestamp, block.data, block.difficulty, block.nonce]))).encode("utf-8")).hexdigest()


def hash_to_binary_str(hash):
    result = ''
    lookup_table = {
        '0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100',
        '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001',
        'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101',
        'e': '1110', 'f': '1111'
    }

    for i in range(len(hash)):
        if lookup_table[hash[i]]:
            result += lookup_table[hash[i]]
        else:
            return None
    
    return result


def hash_matches_difficulty(hash, difficulty):
    hash_in_binary = hash_to_binary_str(hash)
    required_prefix = '0'*difficulty

    return hash_in_binary[0:difficulty] == required_prefix


def add_block(block):
    blockchain.append(block)


def find_block(index, previous_hash, timestamp, data, difficulty):
    nonce = 0
    while 1:
        hash = calculate_hash(index, previous_hash,
                              timestamp, data, difficulty, nonce)
        if hash_matches_difficulty(hash, difficulty):
            return Block(index, hash, previous_hash, timestamp, data, difficulty, nonce)
        nonce += 1


def generate_next_block(data):
    previous_block = get_latest_block()

    difficulty = get_difficulty(get_blockchain())
    print("Difficulty:", difficulty)

    next_index = previous_block.index + 1
    next_timestamp = get_current_timestamp()

    next_block = find_block(next_index, previous_block.hash,
                            next_timestamp, data, difficulty)
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
    return all([is_valid_new_block(blockchain[i], blockchain[i-1]) for i in range(1, len(blockchain))])


def replace_chain(new_blockchain):
    if is_valid_chain(new_blockchain) and len(new_blockchain) > len(get_blockchain()):
        print("Received blockchain is valid. Replacing current blockchain with received blockchain")
        blockchain = new_blockchain
    else:
        print("Received blockchain is invalid")


def get_blockchain():
    return blockchain


def get_serialized_block(block: Block):
    serialized_block = {"index": block.index, "hash": block.hash,
                        "previous hash": block.previous_hash, "timestamp": block.timestamp, "data": block.data}
    return serialized_block


def get_serialized_blockchain():
    serialized_blockchain = list(map(get_serialized_block, blockchain))
    return json.dumps(serialized_blockchain)


def get_readjusted_difficulty(latest_block, a_blockchain):
    prev_adjustment_block = a_blockchain[-DIFFICULTY_ADJUSTMENT_INTERVAL]
    time_expected = BLOCK_GENERATION_INTERVAL * DIFFICULTY_ADJUSTMENT_INTERVAL
    time_taken = latest_block.timestamp - prev_adjustment_block.timestamp

    if time_taken < time_expected/2:
        return prev_adjustment_block.difficulty + 1
    elif time_taken > time_expected/2:
        return prev_adjustment_block.difficulty - 1
    else:
        return prev_adjustment_block.difficulty


def get_difficulty(a_blockchain):
    latest_block = a_blockchain[-1]
    if latest_block.index % DIFFICULTY_ADJUSTMENT_INTERVAL == 0 and latest_block.index != 0:
        return get_readjusted_difficulty(latest_block, a_blockchain)
    else:
        return latest_block.difficulty


def get_current_timestamp():
    return round(time()/1000)
