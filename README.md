# LGB-convertor
[![Pre-commit](https://github.com/Yangruipis/lgb-convertor/actions/workflows/pylint.yml/badge.svg)](https://github.com/Yangruipis/lgb-convertor/actions/workflows/pylint.yml)

lgbc is a tool that convert LightGBM(aka lgb) model to an if-else statement of each language.

**It is useful when deploy a lgb model without LightGBM package.**

## language supported

| date       | lang    | test |
|:----------:|:-------:|:----:|
| 2021-09-21 | python3 |      |
| 2021-09-24 | cpp     |  [![CPP](https://github.com/Yangruipis/lgb-convertor/actions/workflows/cpp.yml/badge.svg)](https://github.com/Yangruipis/lgb-convertor/actions/workflows/cpp.yml)    |
| 2021-09-25 | go      |      |



## install

```bash
git clone https://github.com/Yangruipis/lgb-convertor.git && cd lgb-convertor

python setup.py install
```

## try example

Firstly, you need to dump your lgb model to json format:

```python
model_json = lgb_model.booster_.dump_model()
```

Then, as an input of CLI tool, your need to dump your `model_json` to a local file, such as [example/test_model_tiny.json](example/test_model_tiny.json).

### Python3

```bash
lgbc --model-json example/test_model_tiny.json --lang python3
```

<details>
  <summary><strong>python3 输出</strong></summary>

```python
#
#
# THIS CODE IS GENERATED BY lgb-convertor. DO NOT EDIT IT.
#
# https://github.com/Yangruipis/lgb-convertor
#
# MIT License
#
# Copyright (c) 2021 r.yang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

def predict_tree_0(arr):
    import numpy as np

    if ( arr[0] <= 0.1 ):
        return 0.1
    else:
        if ( arr[0] <= 0.5 ):
            return 0.3
        else:
            if ( np.isnan(arr[1]) or arr[1] in (1,2,3,) ):
                return 0.4
            else:
                return 0.5
```

</details>

### Golang

```bash
lgbc --model-json example/test_model_tiny.json --lang go
```

<details>
  <summary><strong>golang 输出</strong></summary>

```go
//
// THIS CODE IS GENERATED BY lgb-convertor. DO NOT EDIT IT.
//
// https://github.com/Yangruipis/lgb-convertor
//
// MIT License
//
// Copyright (c) 2021 r.yang
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//
package main

import "math"

func predict_tree_0(arr []float64) float64 {

        if arr[0] <= 0.1 {
                return 0.1
        } else {

                if arr[0] <= 0.5 {
                        return 0.3
                } else {

                        if math.IsNaN(arr[1]) || (arr[1] == 1 || arr[1] == 2 || arr[1] == 3) {
                                return 0.4
                        } else {
                                return 0.5
                        }
                }
        }
}

```

</details>

### Cpp

```bash
lgbc --model-json example/test_model_tiny.json --lang cpp
```

<details>
  <summary><strong>cpp 输出</strong></summary>

```cpp

//
// THIS CODE IS GENERATED BY lgb-convertor. DO NOT EDIT IT.
//
// https://github.com/Yangruipis/lgb-convertor
//
// MIT License
//
// Copyright (c) 2021 r.yang
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//

#include <cmath>

float predict_tree_0(float* arr)
{

    if ( arr[0] <= 0.1 )
    {
        return 0.1;
    }
    else
    {

        if ( arr[0] <= 0.5 )
        {
            return 0.3;
        }
        else
        {

            if ( std::isnan(arr[1]) || (arr[1] == 1 || arr[1] == 2 || arr[1] == 3) )
            {
                return 0.4;
            }
            else
            {
                return 0.5;
            }
        }
    }
}
```

</details>

### output:


## run test

```
pip install -r requirements-dev.txt

pytest tests
```

## extends and contributes

### support more language

Please impl your own convertor of the language you need. Below is an example for cpp, you should overwrite those eight `_to_str` functions. More details are in [./lgb_convertor/lang/cpp.py](./lgb_convertor/lang/cpp.py).

```python
from lgb_convertor.base.convertor import BaseConvertor
from lgb_convertor.base.registory import register


@register('cpp')
class CPPConvertor(BaseConvertor):
    def _func_to_str(self, item: FuncStatement):
        pass

    def _if_else_to_str(self, item: IfElseStatement):
        pass

    def _is_null_to_str(self, item: IsNullStatement):
        pass

    def _is_in_to_str(self, item: IsInStatement):
        pass

    def _return_to_str(self, item: ReturnStatement):
        pass

    def _scalar_to_str(self, item: ScalarStatement):
        pass

    def _index_to_str(self, item: IndexStatement):
        pass

    def _condition_to_str(self, item: ConditionStatement):
        pass

```

### code style and static check

```
pre-commit run --all-files --show-diff-on-failure
```
