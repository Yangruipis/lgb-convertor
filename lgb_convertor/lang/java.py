# -*- coding: utf-8 -*-

import os
import sys
from typing import List

from lgb_convertor.base.convertor import BaseConvertor
from lgb_convertor.base.declaration import __declaration__
from lgb_convertor.base.registory import register
from lgb_convertor.base.statement import Op, Statement


@register('java')
class JavaConvertor(BaseConvertor):

    __doc__ = """java code convertor (LLVM style format)
    """

    INDENT = '    '
    OP_MAP = {
        'OR': '||',
        'AND': '&&',
    }

    def _lgb_to_str(self, item):
        declare = '\n'.join(['// ' + i for i in __declaration__.splitlines()])

        trees = '\n'.join([str(tree) for tree in item.trees])
        trees = trees.replace('\n', f'\n{self.INDENT}')
        return str(
            f'{declare}\n'
            f'public class __LGBC_LGBModel {{\n'
            f'{self.INDENT}public static final double NaN = 0.0d / 0.0;\n'
            f'{self.INDENT}{trees}\n'
            f'}}\n'
        )

    def _func_to_str(self, item):
        return str(
            f'private double {item.name}_{item.index}(double[] {",".join(item.args)}) {{\n'
            f'{item.body}\n'
            f'}}\n'
        )

    def _if_else_to_str(self, item):
        tab = self.INDENT * item.depth
        next_tab = self.INDENT * (item.depth + 1)
        return str(
            f'\n'
            f'{tab}if {item.condition} {{\n'
            f'{next_tab}{item.left}\n'
            f'{tab}}} else {{\n'
            f'{next_tab}{item.right}\n'
            f'{tab}}}'
        )

    def _is_null_to_str(self, item):
        return f'Double.isNaN({item.value})'

    def _is_in_to_str(self, item):
        condition_list = [f'Math.abs({item.value} - {i}) <= 1e-6' for i in item.container]
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


_ = JavaConvertor()
