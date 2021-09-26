# -*- coding: utf-8 -*-

import os
import sys
from enum import Enum

from lgb_convertor.base.statement import (
    ConditionStatement,
    FuncStatement,
    IfElseStatement,
    IndexStatement,
    IsInStatement,
    IsNullStatement,
    LGBStatement,
    Op,
    ReturnStatement,
    ScalarStatement,
)


def parse_one_tree(root, index, func_name='predict_tree', input_name='arr'):
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
                        IndexStatement(input_name, node['split_feature']).with_depth(depth),
                    ).with_depth(depth)
                ]
            else:
                postfix_exps = [
                    ScalarStatement(node['threshold']).with_depth(depth),
                    IndexStatement(input_name, node['split_feature']).with_depth(depth),
                    Op(node['decision_type']),
                ]

            if node.get('missing_type') == 'NaN' and node['default_left']:
                postfix_exps += [
                    IsNullStatement(
                        IndexStatement(input_name, node['split_feature']).with_depth(depth)
                    ).with_depth(depth),
                    Op.OR,
                ]

            left = inner(node['left_child'], depth + 1)
            right = inner(node['right_child'], depth + 1)
            condition = ConditionStatement(postfix_exps).with_depth(depth)
            return IfElseStatement(condition, left, right).with_depth(depth)

    return FuncStatement(func_name, index, (input_name,), None, inner(root, 1)).with_depth(0)


def parse_sum_tree(tree_num, func_name='predict_tree', input_name='arr'):
    funcs = [f'{func_name}_{i}({input_name})' for i in range(tree_num)]
    funcs_sum = ' + '.join(funcs)
    return FuncStatement(
        func_name, 'all', (input_name,), None, ReturnStatement(funcs_sum).with_depth(1)
    ).with_depth(0)


def parse_all(trees, func_name='predict_tree', input_name='arr'):
    return LGBStatement(
        [parse_one_tree(tree['tree_structure'], idx, func_name) for idx, tree in enumerate(trees)]
        + [parse_sum_tree(len(trees), func_name, input_name)]
    )
