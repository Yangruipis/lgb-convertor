# -*- coding: utf-8 -*-

from lgb_convertor.base.registory import IConvertor
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
    Statement,
)


class BaseConvertor(IConvertor):
    def _lgb_to_str(self, item: LGBStatement):
        raise NotImplementedError

    def _func_to_str(self, item: FuncStatement):
        raise NotImplementedError

    def _if_else_to_str(self, item: IfElseStatement):
        raise NotImplementedError

    def _is_null_to_str(self, item: IsNullStatement):
        raise NotImplementedError

    def _is_in_to_str(self, item: IsInStatement):
        raise NotImplementedError

    def _return_to_str(self, item: ReturnStatement):
        raise NotImplementedError

    def _scalar_to_str(self, item: ScalarStatement):
        raise NotImplementedError

    def _index_to_str(self, item: IndexStatement):
        raise NotImplementedError

    def _condition_to_str(self, item: ConditionStatement):
        raise NotImplementedError

    def to_str(self, item: Statement):
        func_map = {
            LGBStatement: self._lgb_to_str,
            FuncStatement: self._func_to_str,
            IfElseStatement: self._if_else_to_str,
            IsNullStatement: self._is_null_to_str,
            IsInStatement: self._is_in_to_str,
            ScalarStatement: self._scalar_to_str,
            ReturnStatement: self._return_to_str,
            IndexStatement: self._index_to_str,
            ConditionStatement: self._condition_to_str,
        }
        for cls in func_map:
            if isinstance(item, cls):
                return func_map[cls](item)
        raise ValueError('known statement type: {type(item)}')
