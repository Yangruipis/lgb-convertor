# -*- coding: utf-8 -*-
# @File : __init__.py
# @Author : r.yang
# @Date : Fri Sep 24 11:13:01 2021
# @Description :


from lgb_convertor.base.registory import convertor_registry
from lgb_convertor.lang import *
from lgb_convertor.lgb_convertor import parse_all


def e2e_convert(model_json: dict, lang: str):
    trees = parse_all(model_json['tree_info'])
    with convertor_registry(lang):
        for tree in trees:
            yield tree.__str__()
