from typing import Any, Dict, List, Optional
from time import time
import requests

class Blockchain:
    def __init__(self, model):
        self.current_data = []
        self.chain = []
        self.nodes = set()
        self.model = model
        self.new_block(previous_hash='1', proof=None)

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
            node_chain = get_blockchain_from_node(node)
            length = len(node_chain)

            if length > max_length and self.validate_blockchain(node_chain):
                max_length = length
                new_chain = node_chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof: int, previous_hash: Optional[str]) -> Dict[str, Any]:

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'data': self.current_data,
            'proof': proof,
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
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int) -> int:
        accuracy = 0
        if last_proof != None:
            self.model.set_weights(last_proof)
        while accuracy < .7:
            self.model.fit()
            accuracy = self.model.evaluate()

        return self.model.get_weights()

    @staticmethod
    def validate_proof_of_work(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def get_blockchain_from_node(node):
        response = requests.get(f'http://{node}/chain')

        if response.status_code == 200:
            return response.json()['chain']
        
        return None
