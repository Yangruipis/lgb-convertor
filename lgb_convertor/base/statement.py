# -*- coding: utf-8 -*-

import os
import sys
from enum import Enum

from lgb_convertor.base.registory import convertor_registry
from lgb_convertor.utils import initializer


class WithIndent:
    @property
    def depth(self):
        return self._depth

    def with_depth(self, value):
        self._depth = value
        return self


class Statement(WithIndent):
    def __str__(self):
        return convertor_registry.convertor.to_str(self) or 'UNKNOWN'


class Op(Enum):
    OR = 'or'
    AND = 'and'
    LE = '<='
    LT = '<'
    EQ = '=='
    GE = '>='
    GT = '>'


class ScalarStatement(Statement):
    @initializer
    def __init__(self, value):
        pass


class ReturnStatement(Statement):
    @initializer
    def __init__(self, value):
        pass


class IndexStatement(Statement):
    @initializer
    def __init__(self, container, idx):
        pass


class IsNullStatement(Statement):
    @initializer
    def __init__(self, value):
        pass


class IsInStatement(Statement):
    @initializer
    def __init__(self, container, value):
        pass


class FuncStatement(Statement):
    @initializer
    def __init__(self, name, args, dtypes, body):
        pass


class ConditionStatement(Statement):

    __doc__ = """
    condition statement of LGB non-leaf node

    **LANG** class must impl this to convert this to an condition expression
    """

    @initializer
    def __init__(self, postfix_exps):
        pass


class LGBStatement(Statement):
    @initializer
    def __init__(self, condition, left, right):
        pass
