# -*- coding: utf-8 -*-

import os
import sys
from typing import List

from lgb_convertor.base.convertor import BaseConvertor
from lgb_convertor.base.declaration import __declaration__
from lgb_convertor.base.registory import register
from lgb_convertor.base.statement import Op, Statement


@register('cpp')
class CPPConvertor(BaseConvertor):

    __doc__ = """cpp code convertor (LLVM style format)
    """

    INDENT = '    '
    OP_MAP = {
        'OR': '||',
        'AND': '&&',
    }

    def _func_to_str(self, item):
        declare = ''
        if item.index == 0:
            declare = '\n'.join(['// ' + i for i in __declaration__.splitlines()])
        return str(
            f'{declare}\n\n'
            f'#include <cmath>\n\n'
            f'float {item.name}_{item.index}(float* {",".join(item.args)})\n'
            f'{{\n'
            f'{item.body}\n'
            f'}}\n'
        )

    def _if_else_to_str(self, item):
        tab = self.INDENT * item.depth
        next_tab = self.INDENT * (item.depth + 1)
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

    def _is_null_to_str(self, item):
        return f'std::isnan({item.value})'

    def _is_in_to_str(self, item):
        condition_list = [f'{item.value} == {i}' for i in item.container]
        return f'({" || ".join(condition_list)})'

    def _return_to_str(self, item):
        return f'return {item.value};'

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
                peak_value = self.OP_MAP.get(peak.name, peak.value)
                stack.append(f'( {left} {peak_value} {right} )')
        return str(stack[-1])


_ = CPPConvertor()
