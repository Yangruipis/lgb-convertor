# -*- coding: utf-8 -*-

import os
import sys

import pytest
from lgb_convertor.base.registory import _ConvertorRegistry, convertor_registry


def test_registry():
    with convertor_registry('python3'):
        assert convertor_registry.convertor.__class__.__name__ == 'Python3Convertor'
        with pytest.raises(RuntimeError):
            convertor_registry.set('cpp')

    assert convertor_registry.convertor is None
