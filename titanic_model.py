import numpy as np
from model import Model

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
