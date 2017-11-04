from typing import Any, Dict, List, Optional
from time import time
import requests
import json
import hashlib
from urllib.parse import urlparse

accuracy_threshold = .7

class Blockchain:
    def __init__(self, model):
        self.current_data = []
        self.chain = []
        self.nodes = set()
        self.model = model
        self.new_block(previous_hash='1', proof=None, accuracy=None)

    def register_node(self, address: str) -> None:
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def validate_blockchain(self, chain: List[Dict[str, Any]]) -> bool:
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            if block['previous_hash'] != self.hash(last_block):
                return False

            if not self.validate_proof_of_work(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self) -> bool:
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            node_chain = self.get_blockchain_from_node(node)
            length = len(node_chain)

            if length > max_length and self.validate_blockchain(node_chain):
                max_length = length
                new_chain = node_chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof: int, accuracy: float, previous_hash: Optional[str]) -> Dict[str, Any]:

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'data': self.current_data,
            'proof': proof,
            'accuracy': accuracy,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_data = []
        self.chain.append(block)

        return block

    def new_data(self, X, y) -> int:

        self.current_data.append({
            'X': X,
            'y': y
        })

        return self.last_block['index'] + 1

    def get_all_data(self):
        X = []
        y = []
        for block in self.chain:
            for row in block['data']:
                X.append(row['X'])
                y.append(row['y'])
        return { 'X':X, 'y':y }

    @property
    def last_block(self) -> Dict:
        return self.chain[-1]

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        block_string = json.dumps(block['previous_hash'], sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof) -> int:

        all_data = self.get_all_data()

        if len(all_data['X']) == 0:
            return [None, None]

        self.model.set_training_data(all_data['X'], all_data['y'])

        if last_proof != None:
            frozen_layer = self.get_frozen_layer()
            self.model.freeze_layer(frozen_layer)
            self.model.set_weights(last_proof)

        while not self.validate_proof_of_work(last_proof, self.model.get_weights()):
            self.model.fit()

        return [self.model.get_weights(), self.model.evaluate()[0]]

    def validate_proof_of_work(self, last_proof, proof) -> bool:

        all_data = self.get_all_data()
        self.model.set_training_data(all_data['X'], all_data['y'])

        if last_proof != None:
            frozen_layer = self.get_frozen_layer()
            proof[frozen_layer-1] = last_proof[frozen_layer-1]

        self.model.set_weights(proof)
        evaluation = self.model.evaluate()[0]
        print('Current accuracy', evaluation)
        return evaluation > accuracy_threshold

    def get_frozen_layer(self):
        return (self.last_block['index'] % (len(self.model.get_sizes())-2)) + 1

    def get_blockchain_from_node(self,node):
        response = requests.get(f'http://{node}/chain')

        if response.status_code == 200:
            return response.json()
        
        return None
