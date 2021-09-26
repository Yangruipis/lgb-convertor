# -*- coding: utf-8 -*-

import json
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

N_FEATURES = 11


def random_nan(X):
    X[np.random.rand(*X.shape) > 0.9] = np.nan
    return X


def train():
    X, y = make_classification(n_samples=1000, n_features=N_FEATURES, n_classes=2)
    print(X.shape)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    kbins = KBinsDiscretizer(encode='ordinal', strategy='uniform')
    X_train[:, :10] = kbins.fit_transform(X_train[:, :10])
    X_test[:, :10] = kbins.transform(X_test[:, :10])
    X_train = random_nan(X_train)
    X_test = random_nan(X_test)

    model = LGBMClassifier(
        verbose=1, silent=False, n_estimators=10, max_depth=8, colsample_bytree=0.8
    )
    model.fit(X_train, y_train, categorical_feature=list(range(10)))

    pred_test = model.predict_proba(X_test)[:, 1]
    print('auc@test: ', roc_auc_score(y_test, pred_test))

    def preprocess(data):
        data[:, :10] = kbins.fit_transform(data[:, :10])
        data = random_nan(data)
        return data

    return preprocess, model


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def main():

    preprocess, model = train()
    model_json = model.booster_.dump_model()
    # with open('../test_model.json', 'w') as f:
    #     json.dump(model_json, f, indent=4, sort_keys=True)

    X, _ = make_classification(n_samples=100, n_features=N_FEATURES)
    X = preprocess(X)
    answer = model.predict_proba(X)[:, 1]
    # np.savetxt("../../tests/data/feature.csv", X, delimiter=",")
    # np.savetxt("../../tests/data/lgb_predict.csv", answer, delimiter=",")

    # parse if-else code from model json
    trees = e2e_convert(model_json, 'python3')

    # exec this code
    exec(trees, globals())

    # call the predict function of each tree
    result = [0] * X.shape[0]
    for i in range(len(result)):
        result[i] = eval(f'__LGBC_predict_tree_all(X[{i}])')
        result[i] = sigmoid(result[i])

    print(answer[:5])
    print(result[:5])

    # alignment of this and lgb.predict_proba
    np.testing.assert_array_almost_equal(answer, result)


if __name__ == '__main__':
    main()
