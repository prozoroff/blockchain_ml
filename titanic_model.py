import numpy as np
from model import Model
import copy

columns_to_delete=[1, 6]
check_length = 6

class TitanicModel(Model):
        
    def preprocess_data(self, data):
        copy_data = copy.deepcopy(data)
        for column_to_delete in sorted(columns_to_delete, reverse=True):
            [passenger.pop(column_to_delete) for passenger in copy_data]
        result = [];
        for i in range(len(copy_data)):
            row = copy_data[i]
            if len(row) == check_length:
                row[1] = '1' if row[1] == 'female' else '0'
                result.append(row)
        return np.array(result, dtype=np.float32)

    def get_sizes(self):
        return [6,32,32,2]
