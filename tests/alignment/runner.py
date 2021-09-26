# -*- coding: utf-8 -*-

import argparse
import json
import os
import subprocess
import sys

from lgb_convertor import e2e_convert

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('--lang', default='cpp')
args = parser.parse_args()

TPL = '#CODE_TPL#'


def run_python3(model_json):
    import numpy as np

    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    res = ''
    for tree in e2e_convert(model_json, args.lang):
        res += tree

    X = np.loadtxt(os.path.join(_CURRENT_DIR, '../data/feature.csv'), delimiter=',')
    answer = np.loadtxt(os.path.join(_CURRENT_DIR, '../data/lgb_predict.csv'), delimiter=',')
    exec(res, globals())

    result = [0] * X.shape[0]
    for i in range(len(result)):
        result[i] = eval(f'predict_tree_all(X[{i}])')
        result[i] = sigmoid(result[i])

    for i, v in enumerate(answer):
        print('{:.4f} vs {:.4f}'.format(v, answer[i]))
    np.testing.assert_array_almost_equal(answer, result)


def run_go(model_json):
    res = ''
    for tree in e2e_convert(model_json, args.lang):
        res += tree

    code = open(os.path.join(_CURRENT_DIR, 'alignment.go.tpl')).read()
    code = code.replace(TPL, res)

    file_path = os.path.join(_CURRENT_DIR, 'alignment.go')
    with open(file_path, 'w') as f:
        f.write(code)

    cmd = f'go run {file_path}'
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f'cmd failed: {cmd}')
        raise RuntimeError(res)
    else:
        print(f'cmd({cmd}) successed!')


def run_cpp(model_json):
    res = ''
    for tree in e2e_convert(model_json, args.lang):
        res += tree

    cpp = open(os.path.join(_CURRENT_DIR, 'alignment.cpp.tpl')).read()
    cpp = cpp.replace(TPL, res)

    cpp_file_path = os.path.join(_CURRENT_DIR, 'alignment.cpp')
    with open(cpp_file_path, 'w') as f:
        f.write(cpp)

    cmd = f'g++ {cpp_file_path} -o tmp.bin && ./tmp.bin && rm ./tmp.bin'
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f'cmd failed: {cmd}')
        raise RuntimeError(res)
    else:
        print(f'cmd({cmd}) successed!')


def main():
    model_json = json.load(open(os.path.join(_CURRENT_DIR, '../../example/test_model.json')))
    if args.lang == 'cpp':
        run_cpp(model_json)
    elif args.lang == 'python3':
        run_python3(model_json)
    elif args.lang == 'go':
        run_go(model_json)


if __name__ == '__main__':
    main()
