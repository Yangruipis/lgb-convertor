# -*- coding: utf-8 -*-

import os
import sys
from typing import List

from lgb_convertor.base.declaration import __declaration__
from lgb_convertor.base.registory import IConvertor, register
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
    Statement,
)


@register('python3')
class Python3Convertor(IConvertor):

    INDENT = '    '

    @staticmethod
    def to_str(item):
        assert isinstance(item, Statement)
        tab = Python3Convertor.INDENT * item.depth
        next_tab = Python3Convertor.INDENT * (item.depth + 1)

        if isinstance(item, FuncStatement):
            declare = ''
            if item.index == 0:
                declare = '\n'.join(['# ' + i for i in __declaration__.splitlines()])
            return str(
                f'{declare}\n\n'
                f'def {item.name}_{item.index}({",".join(item.args)}):\n'
                f'{next_tab}import numpy as np\n\n'
                f'{next_tab}{item.body}\n'
            )

        if isinstance(item, LGBStatement):
            return str(
                f'if {item.condition}:\n{next_tab}{item.left}\n{tab}else:\n{next_tab}{item.right}'
            )

        if isinstance(item, IsNullStatement):
            return f'np.isnan({item.value})'

        if isinstance(item, IsInStatement):
            return f'{item.value} in ({",".join(item.container)},)'

        if isinstance(item, ReturnStatement):
            return f'return {item.value}'

        if isinstance(item, ScalarStatement):
            return f'{item.value}'

        if isinstance(item, IndexStatement):
            return f'{item.container}[{item.idx}]'

        if isinstance(item, ConditionStatement):
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
