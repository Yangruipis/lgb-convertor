# -*- coding: utf-8 -*-

import os
import sys
from typing import List

from lgb_convertor.base.convertor import BaseConvertor
from lgb_convertor.base.declaration import __declaration__
from lgb_convertor.base.registory import register
from lgb_convertor.base.statement import (
    ConditionStatement,
    FuncStatement,
    IfElseStatement,
    IndexStatement,
    IsInStatement,
    IsNullStatement,
    Op,
    ReturnStatement,
    ScalarStatement,
    Statement,
)


@register('python3')
class Python3Convertor(BaseConvertor):

    INDENT = '    '

    def _func_to_str(self, item):
        next_tab = self.INDENT * (item.depth + 1)
        declare = ''
        if item.index == 0:
            declare = '\n'.join(['# ' + i for i in __declaration__.splitlines()])
            declare += '\nimport numpy as np\n\n'
        return str(
            f'{declare}\n\n'
            f'def {item.name}_{item.index}({",".join(item.args)}):\n'
            # f'{next_tab}import numpy as np\n\n'
            f'{next_tab}{item.body}\n'
        )

    def _if_else_to_str(self, item):
        tab = self.INDENT * item.depth
        next_tab = self.INDENT * (item.depth + 1)
        return str(
            f'if {item.condition}:\n{next_tab}{item.left}\n{tab}else:\n{next_tab}{item.right}'
        )

    def _is_null_to_str(self, item):
        return f'np.isnan({item.value})'

    def _is_in_to_str(self, item):
        return f'{item.value} in ({",".join(item.container)},)'

    def _return_to_str(self, item):
        return f'return {item.value}'

    def _scalar_to_str(self, item):
        return f'{item.value}'

    def _index_to_str(self, item):
        return f'{item.container}[{item.idx}]'

    def _condition_to_str(self, item):
        postfix_exps = item.postfix_exps[:]
        stack = []
        while postfix_exps:
            peak = postfix_exps.pop(0)
            if isinstance(peak, Statement):
                stack.append(peak)
            else:
                left = stack.pop()
                right = stack.pop()
                assert isinstance(peak, Op)
                stack.append(f'( {left} {peak.value} {right} )')
        return str(stack[-1])


_ = Python3Convertor()
