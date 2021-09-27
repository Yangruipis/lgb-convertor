# -*- coding: utf-8 -*-
# @File : __init__.py
# @Author : r.yang
# @Date : Fri Sep 24 11:13:01 2021
# @Description :


from lgb_convertor.base.registory import convertor_registry
from lgb_convertor.lang import *
from lgb_convertor.lgb_convertor import parse_all
from lgb_convertor.version import __version__


def e2e_convert(model_json: dict, lang: str, func_name='__LGBC_predict_tree'):
    lgb = parse_all(model_json['tree_info'], func_name=func_name)
    with convertor_registry(lang):
        return lgb.__str__()
