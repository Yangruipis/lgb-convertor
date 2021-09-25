# -*- coding: utf-8 -*-

import os
import sys

import numpy as np
from lgb_convertor.base.registory import convertor_registry
from lgb_convertor.base.statement import FuncStatement, IfElseStatement, Statement
from lgb_convertor.lang.cpp import CPPConvertor
from lgb_convertor.lang.python3 import Python3Convertor
from lgb_convertor.lgb_convertor import parse_one_tree

TREE_JSON = {
    'split_feature': 0,
    'threshold': 0.1,
    'decision_type': '<=',
    'left_child': {'leaf_index': 0, 'leaf_value': 0.1,},
    'right_child': {
        'split_feature': 0,
        'threshold': 0.5,
        'decision_type': '<=',
        'left_child': {'leaf_index': 1, 'leaf_value': 0.3,},
        'right_child': {
            'split_feature': 1,
            'threshold': '1||2||3',
            'decision_type': '==',
            'default_left': True,
            'missing_type': 'NaN',
            'left_child': {'leaf_index': 2, 'leaf_value': 0.4,},
            'right_child': {'leaf_index': 3, 'leaf_value': 0.5,},
        },
    },
}


def test_parse_one_tree_python3():
    with convertor_registry('python3'):
        res = parse_one_tree(TREE_JSON, 0)
        print(res)
        exec(str(res))
        assert eval('predict_tree_0([0, 1])') == 0.1
        assert eval('predict_tree_0([0.2, 1])') == 0.3
        assert eval('predict_tree_0([0.6, 1])') == 0.4
        assert eval('predict_tree_0([0.6, 4])') == 0.5


def test_parse_one_tree_cpp():
    with convertor_registry('cpp'):
        res = parse_one_tree(TREE_JSON, 0)
        print(str(res))
