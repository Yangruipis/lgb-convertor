# -*- coding: utf-8 -*-

import os
import pickle
import sys

import numpy as np
import pandas as pd
from lgb_convertor import e2e_convert
from lightgbm import LGBMClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import KBinsDiscretizer


def train():
    X, y = make_classification(n_samples=100)
    print(X.shape)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    kbins = KBinsDiscretizer(encode='ordinal', strategy='uniform')
    X_train[:, :10] = kbins.fit_transform(X_train[:, :10])
    X_test[:, :10] = kbins.transform(X_test[:, :10])

    model = LGBMClassifier(verbose=1, silent=False)
    model.fit(X_train, y_train, categorical_feature=range(10))

    pred_test = model.predict_proba(X_test)[:, 1]
    print('auc@test: ', roc_auc_score(y_test, pred_test))

    def preprocess(data):
        data[:, :10] = kbins.fit_transform(data[:, :10])
        return data

    return preprocess, model


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def main():

    preprocess, model = train()
    model_json = model.booster_.dump_model()

    X, _ = make_classification(n_samples=1000)
    X = preprocess(X)
    answer = model.predict_proba(X)[:, 1]

    # parse if-else code from model json
    trees = e2e_convert(model_json, 'python3')

    # exec this code
    for tree in trees:
        exec(tree)

    # call the predict function of each tree
    result = [0] * X.shape[0]
    for i in range(len(result)):
        for j in range(len(trees)):
            result[i] += eval(f'predict_tree_{j}(X[{i}])')
        result[i] = sigmoid(result[i])

    print(answer[:5])
    print(result[:5])

    # alignment of this and lgb.predict_proba
    np.testing.assert_array_almost_equal(answer, result)


if __name__ == '__main__':
    main()
