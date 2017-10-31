import numpy as np
from model import Model
import random

columns_to_delete=[1, 6]

class TitanicModel(Model):
        
    def preprocess_data(self, data):
        for column_to_delete in sorted(columns_to_delete, reverse=True):
            [passenger.pop(column_to_delete) for passenger in data]
        for i in range(len(data)):
            data[i][1] = 1. if data[i][1] == 'female' else 0.
        return np.array(data, dtype=np.float32)

    def get_sizes(self):
        return [6,32,32,2]


from tflearn.data_utils import load_csv
data, labels = load_csv('titanic_dataset.csv', target_column=0,
                        categorical_labels=True, n_classes=2)


data_length = len(data)
test_size = int(data_length*.1)
eval_indexes = random.sample(range(1, data_length), test_size)

model = TitanicModel()
model.set_training_data(data, labels, eval_indexes)
model.fit()
print(model.evaluate())

weights = model.get_weights();
data, labels = load_csv('titanic_dataset.csv', target_column=0,
                        categorical_labels=True, n_classes=2)

model2 = TitanicModel()
model2.set_training_data(data, labels, eval_indexes)
model2.set_weights(weights)
print(model2.evaluate())
