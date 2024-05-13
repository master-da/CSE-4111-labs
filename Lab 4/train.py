import pandas as pd
import numpy as np
from BinaryClassifier import BinaryClassifier2D

if __name__ == "__main__":
    df = pd.read_csv("./Dataset/Binary-classification-dataset-master/data1/data.csv", header=None, names=['y', 'x1', 'x2'])
    
    binaryClassifier = BinaryClassifier2D(BinaryClassifier2D.architecture)
    
    X = df[['x1', 'x2']].values.T
    
    # st = binaryClassifier.W[:]
    # print(st)
    
    binaryClassifier.fit(X, df[['y']].values, epochs=1000)
    
    # print(binaryClassifier.W)
    # 
    test = pd.read_csv("./Dataset/Binary-classification-dataset-master/data1/test.csv", header=None, names=['y', 'x1', 'x2'])
    # print(test[['x1', 'x2']].values)
    result = binaryClassifier.predict(test[['x1', 'x2']].values.T)
    print(result)
    
    