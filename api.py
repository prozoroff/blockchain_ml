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
    proof_and_accuracy = blockchain.proof_of_work(last_proof)
    block = blockchain.new_block(proof_and_accuracy[0], proof_and_accuracy[1], blockchain.hash(last_block))

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'data_len':  len(block['data']),
        'accuracy': proof_and_accuracy[1],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


@app.route('/data/new', methods=['GET'])
def add_data():
    for i in range(10):
        new_data = get_rand_data()
        index = blockchain.new_data(new_data[0], new_data[1])
    response = {'message': f'Data will be added to Block {index}'}

    return jsonify(response), 201

@app.route('/data/all', methods=['GET'])
def get_data():
    all_data = blockchain.get_all_data()
    response = {'message': str(all_data)}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def get_full_blockchain():
    return jsonify(readable_blockchain()), 200


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

@app.route('/nodes/all', methods=['GET'])
def get_known_nodes():
    return jsonify(list(blockchain.nodes)), 200


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': readable_blockchain()
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': readable_blockchain()
        }

    return jsonify(response), 200

def readable_blockchain():
    return list(map(lambda x: {
            'index': x['index'],
            'timestamp': x['timestamp'],
            'data_len': len(x['data']),
            'accuracy': x['accuracy'],
            'previous_hash': x['previous_hash'],
        }, blockchain.chain))

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)