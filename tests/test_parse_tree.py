# -*- coding: utf-8 -*-

import os
import sys

from lgb_convertor.base.registory import convertor_registry
from lgb_convertor.base.statement import FuncStatement, LGBStatement, Statement
from lgb_convertor.lang.python3 import Python3Convertor
from lgb_convertor.lgb_convertor import parse_one_tree

TREE_JSON = {
    'split_feature': 0,
    'threshold': 0.1,
    'decision_type': '<=',
    'left_child': {'leaf_index': 0, 'leaf_value': 0.1,},
    'right_child': {
        'split_feature': 0,
        'threshold': 0.1,
        'decision_type': '<=',
        'left_child': {'leaf_index': 0, 'leaf_value': 0.1,},
        'right_child': {'leaf_index': 1, 'leaf_value': 0.2,},
    },
}


def test_parse_one_tree():
    with convertor_registry(Python3Convertor()):
        res = parse_one_tree(TREE_JSON, 0)
        print(res)
