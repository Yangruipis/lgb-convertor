# -*- coding: utf-8 -*-

import os
import sys
from enum import Enum

from lgb_convertor.base.statement import (
    ConditionStatement,
    FuncStatement,
    IndexStatement,
    IsNullStatement,
    LGBStatement,
    Op,
    ScalarReturnStatement,
)


def parse_one_tree(root, index, array_type='double', return_type='double'):
    def inner(node, depth):
        if 'leaf_index' in node:
            return ScalarReturnStatement(node['leaf_value']).with_depth(depth)
        else:

            # save as postfix expression
            postfix_exps = []
            postfix_exps += [
                IndexStatement('arr', node['split_feature']).with_depth(depth),
                node['threshold'],
                Op(node['decision_type']),
            ]

            if node.get('missing_type') == 'NaN':
                postfix_exps += [
                    IsNullStatement(IndexStatement('arr', node['split_feature'])).with_depth(depth),
                    Op.OR,
                ]

            left = inner(node['left_child'], depth + 1)
            right = inner(node['right_child'], depth + 1)
            condition = ConditionStatement(postfix_exps).with_depth(depth)
            return LGBStatement(left, right, condition).with_depth(depth)

    return FuncStatement(f'predictTree_{index}', ('arr',), ('float[]',), inner(root, 1)).with_depth(
        0
    )


def parse_all(trees, array_type='double', return_type='double'):
    return [
        parse_one_tree(tree['tree_structure'], idx, array_type, return_type)
        for idx, tree in enumerate(trees)
    ]
