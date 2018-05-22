import json
import random
import time
from datetime import datetime

from apistar import App, Route, http, types

from blockchain import Block, BlockType


# Booststrap our blockchain with a genesis block, set the current state (latest block)
genesis_block = Block(0, datetime.now(), "Well I've been waiting, waiting here so long.", "0")
the_blockchain = [genesis_block]
current_state = genesis_block


def chain() -> dict:
    """
    Returns the entire blockchain.
    """
    return {
        'length': len(the_blockchain),
        'chain': [BlockType(b) for b in the_blockchain]
    }


def add_block(request: http.Request) -> BlockType:
    """
    Adds a new block of arbitrary data to the blockchain.
    Returns the new block on success.
    """

    global current_state
    block_data = json.loads(request.body.decode('utf-8'))
    new_block = Block(
        len(the_blockchain),
        datetime.now(),
        block_data,
        current_state.hash
    )

    the_blockchain.append(new_block)
    current_state = new_block

    return BlockType(new_block)


def validate_chain() -> dict:
    """
    Test endpoint that will recompute the hashes for each block and validate 
    the entire chain.
    """
    start_time = time.time()
    prev_hash = genesis_block.hash
    valid = True

    try:
        for b in the_blockchain[1:]:
            computed_hash = Block._do_hash(b.index, b.timestamp, b.data, prev_hash)
            assert b.hash == computed_hash
            prev_hash = computed_hash
    except AssertionError:
        valid = False
    finally:
        end_time = time.time()
    
    output = {
        'valid': valid,
        'execution_time': end_time - start_time
    }

    if not valid:
        output.update({
            'failed_block': BlockType(b)
        })
    
    return output

def tamper() -> BlockType:
    """
    Test endpoint that will manipulate the data of a random block.  This will
    cause the validation endpoint to fail.
    """
    random_block = random.choice(the_blockchain)
    random_block.data = {
        "foo":  "bar"
    }

    return BlockType(random_block)


routes = [
    Route('/', method='GET', handler=chain),
    Route('/block', method='POST', handler=add_block),
    Route('/validate', method='GET', handler=validate_chain),
    Route('/tamper', method='GET', handler=tamper)
]

app = App(routes=routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
