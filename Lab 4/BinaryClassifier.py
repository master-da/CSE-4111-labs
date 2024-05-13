import numpy as np

class BinaryClassifier2D:
    
    architecture = [
        {'output_dim': 25},  # Input layer
        {'output_dim': 50},
        {'output_dim': 50},
        {'output_dim': 25},
        {'output_dim': 1},  # Output layer
    ]
    
    W = None
    b = None
    cache = None
    learning_rate = 0.1
    
    def __init__(self, architecture):
        
        self.W = []
        self.b = []
        self.cache = {
            'z': [0] * len(architecture),   # z[i] is the output of layer z
            'h': [0] * len(architecture)    # h[i] in the input of layer i
        }
        
        self.W.append(np.random.randn(architecture[0]['output_dim'], 2) * 0.01)
        self.b.append(np.random.randn(architecture[0]['output_dim'], 1) * 0.01)
        

        for i in range(1, len(architecture)):
            self.W.append(np.random.randn(architecture[i]['output_dim'], architecture[i-1]['output_dim']) * 0.01)
            self.b.append(np.random.randn(architecture[i]['output_dim'], 1) * 0.01)

            
    def sigmoid(self, Z):
        return 1 / (1 + np.exp(-Z))
    
    def backward_signmoid(self, dA, Z):
        return dA * self.sigmoid(Z) * (1 - self.sigmoid(Z))
    
    def forward_propagation(self, X, debug=False):
        if debug: print(f'Layer 0 h: {X}')
        h_i = X
        for i in range(len(self.W)):

            self.cache['h'][i] = h_i
            
            z_i = np.dot(self.W[i], h_i) + self.b[i]
            h_i = self.sigmoid(z_i)

            if debug: print(f'Layer {i} h: {h_i}')

            self.cache['z'][i] = z_i
            
        return h_i
    
    def loss(self, y, y_hat):
        shape = y_hat.shape[1]
        return np.squeeze(-1/shape * np.sum(y * np.log(y_hat) +(1 - y) * np.log(1 - y_hat)))    

    def backward_propagation(self, X, y, y_hat):
               
        shape = y.shape[1]
        y = y.reshape(y_hat.shape)
            
        dA = - (np.divide(y, y_hat) - np.divide(1 - y, 1 - y_hat))
                
        for i in reversed(range(len(self.W))):
            
            dZ = self.backward_signmoid(dA, self.cache['z'][i])
            dW = 1/shape * np.dot(dZ, self.cache['h'][i].T)
            db = 1/shape * np.sum(dZ, axis=1, keepdims=True)
            dA = np.dot(self.W[i].T, dZ)
            
            self.W[i] = self.W[i] - self.learning_rate * dW
            self.b[i] = self.b[i] - self.learning_rate * db
                        
    def fit(self, X, y, epochs=100):
        print(self.W)
        for i in range(epochs):
            
            y_hat = self.forward_propagation(X)
            loss = self.loss(y, y_hat)
            # print(y_hat)
            # print(loss)
            self.backward_propagation(X, y, y_hat)
            
            # if i % 10 == 0:
            #     print(f'Epoch {i} - Loss: {loss}')
        print(self.W)
        


                
    def predict(self, X):
        return self.forward_propagation(X)
