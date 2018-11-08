from flask import Flask, jsonify, url_for, request
from argparse import ArgumentParser
from blockchain import BlockChain
from uuid import uuid4
import requests

web_app = Flask(__name__)

blockchain = BlockChain()

node_address = uuid4().hex


@web_app.route('/transactions/new', methods=['POST'])
def create_transaction():
    # Accepting Payload from user in JSON content type
    transaction_data = request.get_json()
    index = blockchain.create_new_transaction(**transaction_data)
    response = {
        'message': 'Transaction has been submitted successfully',
        'block_index': index
    }
    return jsonify(response), 201


@web_app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_block(node_address)
    response = {
        'message': 'Successfully mined the new block',
        'block_data': block
    }
    return jsonify(response)


@web_app.route('/chain', methods=['GET'])
def get_full_chain():
    response = {
        'chain': blockchain.get_serialized_chain
    }
    return jsonify(response)


@web_app.route('/nodes/register', methods=['POST'])
def register_node():
    node_data = request.get_json()
    blockchain.create_node(node_data.get('address'))
    response = {
        'message': 'New node has been added',
        'node_count': len(blockchain.nodes),
        'nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


def get_neighbour_chains():
    neighbour_chains = []
    for node_address in blockchain.nodes:
        res = requests.get(node_address + url_for('get_full_chain')).json()
        chain = res['chain']
        neighbour_chains.append(chain)
    return neighbour_chains


@web_app.route('/consensus', methods=['GET'])
def sync_chain():
    neighbour_chains = get_neighbour_chains()
    if not neighbour_chains:
        return jsonify({'message': 'No neighbour chain is available'})

    # Get the longest chain
    longest_chain = max(neighbour_chains, key=len)

    # If our chain is longest, then do nothing
    if len(blockchain.chain) >= len(longest_chain):
        response = {
            'message': 'Chain is already up to date',
            'chain': blockchain.get_serialized_chain
        }
    # If our chain isn't longest, then we store the longest chain
    else:
        blockchain.chain = [blockchain.get_block_object_from_block_data(block) for block in longest_chain]
        response = {
            'message': 'Chain was replaced',
            'chain': blockchain.get_serialized_chain
        }

    return jsonify(response)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=64037, type=int)
    args = parser.parse_args()

    web_app.run(host=args.host, port=args.port, debug=True)
