import sklearn 
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data(train = 'training.csv', test = 'testing.csv'):
    
    test = pd.read_csv(test, header = None)
    test.columns = ['open', 'high', 'low', 'close']
    t = pd.read_csv(train, header = None)
    t.columns = ['open', 'high', 'low', 'close']
    return t,test

def train_model(t, test):
    
    
    t['y'] = t['open'].shift(-1)
    t.fillna(method='pad',inplace=True)
    x_name = ['open', 'high', 'low', 'close']
    x = t[x_name].values
    y = t[['y']].values
    model = linear_model.LinearRegression()
    model.fit(x,y)
    return model

def make_window(window_size, start_point):
    return [start_point+x for x in range(window_size)]