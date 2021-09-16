# -*- coding: utf-8 -*-

import os
import sys

from lgb_convertor.base.statement import FuncStatement
from lgb_convertor.lang.lang import Lang


class Python3(Lang):

    INDENT = '\t'

    def convert(self, tree: FuncStatement):
        pass
