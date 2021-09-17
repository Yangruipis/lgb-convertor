# -*- coding: utf-8 -*-

import os
import sys
from typing import List

from lgb_convertor.base.registory import convertor_registry
from lgb_convertor.base.statement import (
    ConditionStatement,
    FuncStatement,
    IndexStatement,
    IsNullStatement,
    LGBStatement,
    Op,
    ScalarReturnStatement,
    ScalarStatement,
    Statement,
)
from lgb_convertor.lang.lang import Lang


class Python3Convertor:

    INDENT = '    '

    @staticmethod
    def to_str(item):
        assert isinstance(item, Statement)
        tab = Python3Convertor.INDENT * item.depth
        next_tab = Python3Convertor.INDENT * (item.depth + 1)

        if isinstance(item, FuncStatement):
            return f'def {item.name}({",".join(item.args)}):\n{next_tab}{item.body}\n'

        if isinstance(item, LGBStatement):
            return (
                f'if {item.condition}:\n{next_tab}{item.left}\n{tab}else:\n{next_tab}{item.right}'
            )

        if isinstance(item, IsNullStatement):
            return f'np.isnan({item.element})'

        if isinstance(item, ScalarReturnStatement):
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
            return stack[-1]


class Python3(Lang):
    @property
    def convertor(self):
        return Python3Convertor()

    def convert(self, trees: List[FuncStatement]):

        with convertor_registry(self.convertor):
            return trees[0].__str__()
