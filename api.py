import hashlib
import json
from urllib.parse import urlparse
from uuid import uuid4
from blockchain import Blockchain
import requests
from flask import Flask, jsonify, request
from titanic_model import TitanicModel
import random

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain(TitanicModel())

from tflearn.data_utils import load_csv
data, labels = load_csv('titanic_dataset.csv', target_column=0,
                        categorical_labels=True, n_classes=2)

def get_rand_data():
    i = random.randint(0,len(data))
    return [data[i], labels[i]]


@app.route('/mine', methods=['GET'])
def mine():

    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'data': block['data'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/data/new', methods=['GET'])
def add_data():
    new_data = get_rand_data()
    index = blockchain.new_data(new_data[0], new_data[1])
    response = {'message': f'Data will be added to Block {index}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def get_full_blockchain():
    return jsonify(blockchain.chain), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)