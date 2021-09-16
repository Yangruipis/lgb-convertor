# -*- coding: utf-8 -*-

import os
import sys

import pytest
from lgb_convertor.base.registory import _ConvertorRegistry, convertor_registry


def test_registry():
    with convertor_registry(1):
        assert convertor_registry.convertor == 1
        with pytest.raises(RuntimeError):
            convertor_registry.set(2)

    assert convertor_registry.convertor is None
