# -*- coding: utf-8 -*-

import os
import sys
from typing import List

from lgb_convertor.base.registory import convertor_registry
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
from lgb_convertor.lang.lang import Lang


class CPPConvertor:

    __doc__ = """cpp code convertor (LLVM style format)
    """

    INDENT = '    '
    OP_MAP = {
        'OR': '||',
        'AND': '&&',
    }

    @staticmethod
    def to_str(item):
        assert isinstance(item, Statement)
        tab = CPPConvertor.INDENT * item.depth
        next_tab = CPPConvertor.INDENT * (item.depth + 1)

        if isinstance(item, FuncStatement):
            return str(
                f'float {item.name}(float[] {",".join(item.args)})\n'
                f'{{\n'
                f'{item.body}\n'
                f'}}\n'
            )

        if isinstance(item, LGBStatement):
            return str(
                f'\n'
                f'{tab}if {item.condition}\n'
                f'{tab}{{\n'
                f'{next_tab}{item.left}\n'
                f'{tab}}}\n'
                f'{tab}else\n'
                f'{tab}{{\n'
                f'{next_tab}{item.right}\n'
                f'{tab}}}'
            )

        if isinstance(item, IsNullStatement):
            return f'std::isnan({item.value})'

        if isinstance(item, IsInStatement):
            condition_list = [f'{item.value} == {i}' for i in item.container]
            return f'({" || ".join(condition_list)})'

        if isinstance(item, ReturnStatement):
            return f'return {item.value};'

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
                    peak_value = CPPConvertor.OP_MAP.get(peak.name, peak.value)
                    stack.append(f'( {left} {peak_value} {right} )')
            return str(stack[-1])


class CPP(Lang):
    @property
    def convertor(self):
        return CPPConvertor()

    def convert(self, trees: List[FuncStatement]):

        with convertor_registry(self.convertor):
            return trees[0].__str__()
