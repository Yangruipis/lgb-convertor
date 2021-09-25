# -*- coding: utf-8 -*-

import json
import os
import sys
import subprocess

import argparse

from lgb_convertor import e2e_convert

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('--lang', default='cpp')
args = parser.parse_args()

TPL = "#CODE_TPL#"

def run_cpp(model_json):
    res = ""
    for tree in e2e_convert(model_json, args.lang):
        res += tree

    cpp = open(os.path.join(_CURRENT_DIR, 'alignment.cpp.tpl')).read()
    cpp = cpp.replace(TPL, res)

    cpp_file_path = os.path.join(_CURRENT_DIR, 'alignment.cpp')
    with open(cpp_file_path, 'w') as f:
        f.write(cpp)

    cmd = f"g++ {cpp_file_path} -o tmp.bin && ./tmp.bin && rm ./tmp.bin"
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f'cmd failed: {cmd}')
        raise RuntimeError(res)
    else:
        print(f'cmd({cmd}) successed!')
    

def main():
    model_json = json.load(
        open(os.path.join(_CURRENT_DIR, "../../example/test_model.json")))
    if args.lang == 'cpp':
        run_cpp(model_json)


if __name__ == "__main__":
    main()
