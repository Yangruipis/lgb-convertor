# -*- coding: utf-8 -*-

import os
import sys
from functools import wraps
from typing import Dict


class IConvertor:
    @staticmethod
    def to_str(item):
        raise NotImplementedError


class _ConvertorRegistry:

    convertor = None
    _lock = False

    _convertors: Dict[str, IConvertor] = {}

    def register(self, name, cls):
        self.acquire()
        self._convertors[name] = cls
        self.release()

    def set(self, convertor):
        self.acquire()
        _ConvertorRegistry.convertor = convertor

    def acquire(self):
        if self._lock:
            raise RuntimeError
        self._lock = True

    def release(self):
        self._lock = False
        _ConvertorRegistry.convertor = None

    def __call__(self, convertor):
        if isinstance(convertor, str):
            convertor = self._convertors[convertor]
        assert isinstance(convertor, IConvertor)
        self.set(convertor)
        return self

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.release()


convertor_registry = _ConvertorRegistry()


def register(name):
    def _register(cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            instance = cls(*args, **kwargs)
            convertor_registry.register(name, instance)
            return instance

        return wrapper

    return _register
