import unittest
from blockchain import Blockchain
from fake_model import FakeModel

class TestBlockchain(unittest.TestCase):

	def test_constructor(self):
		blockchain = Blockchain(FakeModel())
		self.assertEqual(len(blockchain.get_all_data()['y']), 0)
		self.assertEqual(blockchain.last_block['index'], 1)

	def test_new_data(self):
		blockchain = Blockchain(FakeModel())
		blockchain.new_data([0,0], 0)
		self.assertEqual(blockchain.current_data[0]['y'], 0)
		self.assertEqual(blockchain.current_data[0]['X'], [0,0])

	def test_new_block(self):
		blockchain = Blockchain(FakeModel())
		blockchain.new_data([1,1], 1)
		proof = blockchain.proof_of_work(None)
		blockchain.new_block(proof, blockchain.last_block['previous_hash'])
		self.assertEqual(blockchain.get_all_data()['y'][0], 1)
		self.assertEqual(blockchain.get_all_data()['X'][0], [1,1])



if __name__ == '__main__':
	unittest.main()