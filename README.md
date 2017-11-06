# blockchain_ml
Experiments on blockchained machine learning.

Instead of finding a nonce - training the neural network on the data from the previous blocks. Proof of work is the array of neurons weights and biases which satisfy desired loss (accuracy) on available test data. Neural network is used as one-way function. The declared accuracy is easy for any node to verify using weights array. 

To start a node (default port):

```
python api.py
```

To start a node (specific port):

```
python api.py -p 5001
```

### Interacting with Blockchain

To add new data for learning (randomly selected) - GET request to:

```
http://localhost:5000/data/new
```

```
{
    "message": "Data will be added to Block 3"
}
```

To mine new block - GET request to:

```
http://localhost:5000/mine
```

```
{
    "accuracy": 0.7142857313156128,
    "data_len": 40,
    "index": 3,
    "message": "New Block Forged",
    "previous_hash": "1d6a362824666a8917940ee5541b00c3f893d2ce1fe68a9983456582d7023ab1"
}
```

To get current blockchain - GET request to:

```
http://localhost:5000/chain
```

### Registering new Nodes

To register new nodes - POST request to:

```
http://localhost:5000/nodes/register
```

with JSON data: 

```
{
	nodes: [
	    'http://localhost:5001',
	    'http://localhost:5002',
	    ...
	    ]
}
```

To run consensus to ensure a node has the correct chain - GET request to:

```
http://localhost:5000/nodes/resolve
```
