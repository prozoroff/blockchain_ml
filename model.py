
import numpy as np
import tensorflow as tf
import tflearn

eval_share = .1

class Model:
    def __init__(self):
        self.create_dnn(self.get_sizes())

    def set_training_data(self, data, labels, eval_indexes):
        self.data = self.preprocess_data(data)
        self.labels = labels
        self.eval_indexes = eval_indexes
        self.fill_datasets()

    def get_sizes(self):
        return []
        
    def preprocess_data(self, data):
        pass

    def fit(self):
        self.dnn.fit(self.train_X, self.train_y, n_epoch=10, validation_set=0.1, show_metric=False)

    def evaluate(self):
        return self.dnn.evaluate(self.test_X, self.test_y)

    def predict(self, X):
        return self.dnn.predict_label(X)

    def get_weights(self):
        weights = []
        for layer in self.config:
            weights.append([self.dnn.get_weights(layer.W), self.dnn.get_weights(layer.b)])
        return weights

    def set_weights(self, weights):
        for i in range(len(weights)):
            self.dnn.set_weights(self.config[i].W, weights[i][0])
            self.dnn.set_weights(self.config[i].b, weights[i][1])

    def fill_datasets(self):
        train_X = []
        train_y = []
        test_X = []
        test_y = []
        for i in range(len(self.data)):
            if i in self.eval_indexes:
                test_X.append(self.data[i])
                test_y.append(self.labels[i])
            else:
                train_X.append(self.data[i])
                train_y.append(self.labels[i])
        self.train_X = np.array(train_X, dtype=np.float32)
        self.train_y = np.array(train_y, dtype=np.float32)
        self.test_X = np.array(test_X, dtype=np.float32)
        self.test_y = np.array(test_y, dtype=np.float32)

    def create_dnn(self, sizes):
        tf.reset_default_graph()
        ipt = tflearn.input_data(shape=[None, sizes[0]])
        config = []

        if len(sizes) > 2:
            config.append(tflearn.fully_connected(ipt, sizes[1]))
            for i in range(1, len(sizes)-2):
                config.append(tflearn.fully_connected(config[-1], sizes[i+1]))

        out = tflearn.fully_connected(config[-1], sizes[-1], activation='softmax')
        config.append(out)

        self.config = config
        self.dnn = tflearn.DNN(tflearn.regression(out))