# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--lang', default='python3')
parser.add_argument('--model-json',)
args = parser.parse_args()


from lgb_convertor.lang.python3 import Python3
from lgb_convertor.lgb_convertor import parse_all


def main():
    model_json = json.load(open(args.model_json))
    trees = parse_all(model_json['tree_info'])
    code = Python3().convert(trees)
    print(code)


if __name__ == '__main__':
    main()
