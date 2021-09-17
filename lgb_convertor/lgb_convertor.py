# -*- coding: utf-8 -*-

import os
import sys
from enum import Enum

from lgb_convertor.base.statement import (
    ConditionStatement,
    FuncStatement,
    IndexStatement,
    IsInStatement,
    IsNullStatement,
    LGBStatement,
    Op,
    ReturnStatement,
    ScalarStatement,
)


def parse_one_tree(
    root, index, array_type='double', return_type='double', func_name='predict_tree'
):
    def inner(node, depth):
        if 'leaf_index' in node:
            return ReturnStatement(
                ScalarStatement(node['leaf_value']).with_depth(depth)
            ).with_depth(depth)
        else:

            # save as postfix expression
            if isinstance(node['threshold'], str) and '||' in node['threshold']:
                postfix_exps = [
                    IsInStatement(
                        node['threshold'].split('||'),
                        IndexStatement('arr', node['split_feature']).with_depth(depth),
                    ).with_depth(depth)
                ]
            else:
                postfix_exps = [
                    ScalarStatement(node['threshold']).with_depth(depth),
                    IndexStatement('arr', node['split_feature']).with_depth(depth),
                    Op(node['decision_type']),
                ]

            if node.get('missing_type') == 'NaN' and node['default_left']:
                postfix_exps += [
                    IsNullStatement(IndexStatement('arr', node['split_feature'])).with_depth(depth),
                    Op.OR,
                ]

            left = inner(node['left_child'], depth + 1)
            right = inner(node['right_child'], depth + 1)
            condition = ConditionStatement(postfix_exps).with_depth(depth)
            return LGBStatement(condition, left, right).with_depth(depth)

    return FuncStatement(f'{func_name}_{index}', ('arr',), ('float[]',), inner(root, 1)).with_depth(
        0
    )


def parse_all(trees, array_type='double', return_type='double'):
    return [
        parse_one_tree(tree['tree_structure'], idx, array_type, return_type)
        for idx, tree in enumerate(trees)
    ]
