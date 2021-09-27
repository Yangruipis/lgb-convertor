# LGB-convertor
[![Pre-commit](https://github.com/Yangruipis/lgb-convertor/actions/workflows/pylint.yml/badge.svg?branch=master)](https://github.com/Yangruipis/lgb-convertor/actions/workflows/pylint.yml)

lgbc is a tool that converts [LightGBM](https://github.com/microsoft/LightGBM)(aka lgb) model to if-else statements of each language.

**It is useful when deploying a LGB model with no LightGBM packages or any other 3rd party dependency required.** For example, as a spark UDF runs on cluster worker nodes, or on mobile perhaps.

## language supported

| date       | lang    | test |
|:----------:|:-------:|:----:|
| 2021-09-21 | python3 |  [![PYTHON3](https://github.com/Yangruipis/lgb-convertor/actions/workflows/python3.yml/badge.svg?branch=master)](https://github.com/Yangruipis/lgb-convertor/actions/workflows/python3.yml)    |
| 2021-09-24 | c++     |  [![CPP](https://github.com/Yangruipis/lgb-convertor/actions/workflows/cpp.yml/badge.svg)](https://github.com/Yangruipis/lgb-convertor/actions/workflows/cpp.yml)    |
| 2021-09-25 | golang   |  [![GO](https://github.com/Yangruipis/lgb-convertor/actions/workflows/go.yml/badge.svg?branch=master)](https://github.com/Yangruipis/lgb-convertor/actions/workflows/go.yml)    |
| 2021-09-26 | java    |  [![JAVA](https://github.com/Yangruipis/lgb-convertor/actions/workflows/java.yml/badge.svg?branch=master)](https://github.com/Yangruipis/lgb-convertor/actions/workflows/java.yml)    |
| `TODO` | C\#    |      |
| `TODO` |  R   |      |
| `TODO` |  Scala   |      |

## install

```bash
git clone https://github.com/Yangruipis/lgb-convertor.git && cd lgb-convertor

python setup.py install
```

## some examples

Firstly, your LGB model is supposed to be dumped as a dict:

```python
from lightgbm import LGBMClassifier

# train your model here
lgb_model = LGBMClassifier(...)
lgb_model.fit(...)

model_json = lgb_model.booster_.dump_model()
```

Then, if you are going to deploy with python3, just import the lgbc packages.

```python
from lgb_convertor import e2e_convert

# parse model_json with lgbc
lgb_statements = e2e_convert(model_json, 'python3')

# load these funcs globally
exec(lgb_statements, globals())

# mock one sample, assume that we have 100 features
X = np.random.rand(100)

# LGB predict on X
result = eval(f'__LGBC_predict_tree_all(X)')
```

Also, if you wanna convert it to other languages instead of python3, you should call it as an command line tool. Dump your `model_json`, just like [example/test_model_tiny.json](example/test_model_tiny.json).

```python
import json
with open('/YOUR/MODEL_JSON/PATH', 'w') as f:
    json.dump(model_json, f, indent=4)
```

Then, you call use the lgbc command line as follow:

```
usage: lgbc [-h] [--lang LANG] --model-json MODEL_JSON [-v]

Description:
============
lgbc is a tool that convert LightGBM(aka lgb) model to
    if-else statements of each language.

Examples:
=========
- lgbc --model-json example/test_model_tiny.json --lang python3
- lgbc -m example/test_model_tiny.json -l cpp

See more at [https://github.com/Yangruipis/lgb-convertor]

optional arguments:
  -h, --help            show this help message and exit
  --lang LANG, -l LANG  language to convert
  --model-json MODEL_JSON, -m MODEL_JSON
                        lightgbm model json, dumped by `lgb_model.booster_.dump_model()`
  -v, --version         show program's version number and exit
```


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


### Java

```bash
lgbc --model-json example/test_model_tiny.json --lang java
```

<details>
  <summary><strong>Java 输出</strong></summary>


```java
//
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
public class LGBConvertor {
    public static final double NaN = 0.0d / 0.0;
    private double predict_tree_0(double[] arr) {

        if ( arr[0] <= 0.1 ) {
            return 0.1;
        } else {

            if ( arr[0] <= 0.5 ) {
                return 0.3;
            } else {

                if ( Double.isNaN(arr[1]) || (Math.abs(arr[1] - 1) <= 1e-6 || Math.abs(arr[1] - 2) <= 1e-6 || Math.abs(arr[1] - 3) <= 1e-6) ) {
                    return 0.4;
                } else {
                    return 0.5;
                }
            }
        }
    }

    private double predict_tree_all(double[] arr) {
    return predict_tree_0(arr);
    }

}

```

</details>

## run test

```
pip install -r requirements-dev.txt

pytest tests
```

## extends and contributes

### support more language

Please impl your own convertor of the language you need. Below is an example for cpp, you should overwrite those nine `_to_str` functions. More details are in [./lgb_convertor/lang/cpp.py](./lgb_convertor/lang/cpp.py).

```python
from lgb_convertor.base.convertor import BaseConvertor
from lgb_convertor.base.registory import register


@register('cpp')
class CPPConvertor(BaseConvertor):

    def _lgb_to_str(self, item: LGBStatement):
        pass

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
