import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import random
import visualize as vis

'''
def loaddataset()
    if(lensys.argv)!=3):
        print("Usage: python", sys.argv[0], "<input file> <output file>.")
        exit(1)
    return sys.argv[1],sys.argv[2]
'''
#open and print dataset



def stepFunction(weighted_sum):
    if weighted_sum > 0:
        return 1
    else:
        return -1


def predict(weights, input_data,labels):
    weighted_sum = 0
    c = 0.01
    for epoch in range(50):
        for i in range(len(input_data)):
            weighted_sum += np.dot(weights,input_data[i]) 
            prediction = (stepFunction(weighted_sum))
            error = labels[i] - prediction
            if error <= 0:
                weights += error * c * input_data[i]
    
            

def main():
    #Read input file and convert it into a dataset
    inputfile = sys.argv[1]
    dataset = pd.read_csv(inputfile, header = None )
    data = dataset.values
    #the label is the last column of the dataset
    labels = data[:,-1]
    df = pd.DataFrame(dataset)
    input_data = data[:,[0,1]]
    weights = np.random.rand(1,2) 
    predict(weights,input_data,labels)   
    vis.visualize_scatter(df, feat1=0, feat2=1, labels=2)

if __name__ == "__main__":
    main()