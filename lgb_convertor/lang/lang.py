# -*- coding: utf-8 -*-

import os
import sys


class Lang:
    @property
    def convertor(self):
        raise NotImplementedError

    def convert(self, trees):
        raise NotImplementedError
