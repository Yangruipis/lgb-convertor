# -*- coding: utf-8 -*-

import os
import sys


class _ConvertorRegistry:

    convertor = None
    _lock = False

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
        self.set(convertor)
        return self

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.release()


convertor_registry = _ConvertorRegistry()
