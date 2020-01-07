import pandas as pd
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import visualize as vis
ALPHAS = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.98]
DEFAULT_MAX_LIST = [100, 100, 100, 100, 100, 100, 100, 100, 100, 58]
'''
def gradient_descent(X, Y, alpha, max_iter=DEFAULT_MAX[0]):
    n = len(Y)
    beta = np.zeros(len(X[0]))

    for _ in xrange(max_iter):
        f_x = beta.dot(X.T)
        gradient = X.T.dot((f_x - Y)) * alpha / n
        beta -= gradient

    loss = beta.dot(X.T) - Y
    return beta, loss.dot(loss.T) / (2 * n)
'''
def scaling(x, std, mean):
    x_scale = (x-mean)/std
    return x_scale

def main():
    #Read input file and convert it into a dataset
    inputfile = sys.argv[1]
    dataset = pd.read_csv(inputfile, header = None )
    
    #add a column of ones the start for bias
    dataset.insert(0, "New Column", 1)
    df = pd.DataFrame(dataset)
    print(df)
    cols = list(df)
    feature1_mean = np.mean(df[0])
    feature2_mean = np.mean(df[1])
    feature3_mean = np.mean(df[2])
    feature1_std = np.std(df[0])
    feature2_std = np.std(df[1])
    feature3_std = np.std(df[2])
    feature1_scaled = scaling(df[0], feature1_std, feature1_mean)
    feature2_scaled = scaling(df[1], feature2_std, feature2_mean)
    feature3_scaled = scaling(df[2], feature3_std, feature3_mean)
    print("The mean for feature 1 is ", feature1_mean)
    print("The mean for feature 2 is ", feature2_mean)
    print("The mean for feature 3 is ", feature3_mean)
    print("The standard deviation for feature 1 is:" , feature1_std)
    print("The standard deviation for feature 1 is:" , feature2_std)
    print("The standard deviation for feature 1 is:" , feature3_std)
    #print("The scale feature1 is: ", feature1_scaled)
    print("The mean of scale feature1 is ", np.mean(feature1_scaled))
    print("The mean of scale feature2 is ", np.mean(feature2_scaled))
    print("The mean of scale feature3 is ", np.mean(feature3_scaled))
    #print("The scale feature2 is: ", feature2_scaled)
    #print("The scale feature3 is: ", feature3_scaled)
    feature_1 = dataset.iloc[:, 1]
    feature_2 = dataset.iloc[:, 2]
    Y = dataset.iloc[:, 3]
    
    
    m = 0
    k = 0
    c = 0
    n = len(df)
    L = 0.001
    epochs = 100;
    
    #performing gradient descent
    for i in range(epochs): 
        Y_pred = m*feature_1 + n*feature_2 + c  # The current predicted value of Y
        D_m = (-2/n) * sum(feature_1 * (Y - Y_pred)) # Derivative wrt m
        D_k = (-2/n) * sum(feature_2 * (Y - Y_pred)) # Derivative wrt k
        D_c = (-2/n) * sum(Y - Y_pred)  # Derivative wrt c
        m = m - L * D_m  # Update m
        k = k - L * D_k  # Update k
        c = c - L * D_c  # Update c
    print(m,k,c)
    Y_pred = m*feature_1 + k*feature_2 + c
    
    lin_reg_weights = [m, k, c]
    vis.visualize_3d(df, lin_reg_weights=lin_reg_weights,
                    feat1=0, feat2= 1 , labels=2,
                    xlabel=cols[1], ylabel=cols[2], zlabel=cols[3])
    
    plt.show()
    
if __name__ == "__main__":
    main()