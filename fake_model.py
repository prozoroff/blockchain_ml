from model import Model

class FakeModel(Model):

    def create_dnn(self, sizes):
        pass

    def fit(self):
        pass

    def evaluate(self):
        return .9

    def get_weights(self):
        return [[[0,0],[0,0]],[0,0]]