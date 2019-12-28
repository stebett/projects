import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.special import expit

colnames = []
for i in range(1, 21):
    for k in range(1, 21):
        colnames.append('pix{}x{}'.format(i, k))

X = pd.read_csv('X.csv', names=colnames, header=None)
y = pd.read_csv('y.csv', names=['Target'])


def show_digit(row_num):
    plt.imshow(np.array(
        X[row_num-1:row_num].values.reshape([20, 20]),
        dtype='float'), cmap='gray')


def LogReg(X, y):
    return


def CostFun(theta, x, y, target, activation):
    new_y = y['Target'] == target
    J = (1/X.shape[0])*(np.dot(np.log(activation(np.dot(x, theta))).transpose(), - new_y)
            - np.dot(np.log(1-activation(np.dot(x, theta))).transpose(), (1-new_y)))
    return J





