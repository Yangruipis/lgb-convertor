# LGB-convertor

lgbc is a tool that convert LightGBM(aka lgb) model to an if-else statement of each language. It is useful when deploy a LightGBM model without LightGBM package.


## install

```bash
git clone https://github.com/Yangruipis/lgb-convertor.git && cd lgb-convertor

python setup.py install
```

## try example

```bash

lgbc --model-json example/test_model.json --lang python3
```

### output:

```python
def predict_tree_0(arr):
    if ( arr[0] <= 2.5000000000000004 ):
        if ( arr[2] <= 37.50000000000001 ):
            if ( arr[0] <= 1.0000000180025095e-35 ):
                if ( arr[2] <= 8.500000000000002 ):
                    if ( arr[1] <= 1.0000000180025095e-35 ):
                        return -1.2509164148733616
                    else:
                        if ( arr[1] <= 35.50000000000001 ):
                            return -1.3135338337282139
                        else:
                            if ( arr[1] <= 129.50000000000003 ):
                                if ( arr[1] <= 94.50000000000001 ):
                                    if ( arr[1] <= 56.50000000000001 ):
                                        return -1.279350048356234
                                    else:
                                        if ( arr[1] <= 75.50000000000001 ):
                                            return -1.1668214051304915
                                        else:
                                            return -1.2634369068899671
                                else:
                                    return -1.1043054922273012
                            else:
                                if ( arr[1] <= 587.0000000000001 ):
                                    if ( arr[1] <= 297.50000000000006 ):
                                        return -1.2642924521300891
                                    else:
                                        return -1.3960464191088555
                                else:
                                    return -1.271901343840109
                else:
                    if ( arr[1] <= 24.500000000000004 ):
                        if ( arr[2] <= 16.500000000000004 ):
                            if ( arr[1] <= 1.0000000180025095e-35 ):
                                return -1.232671500055185
                            else:
                                return -1.3297416629994114
                        else:
                            if ( arr[1] <= 1.0000000180025095e-35 ):
                                return -1.3960464191088555
                            else:
                                return -1.3085241410443893
                    else:
                        return -1.3647884626572604
            else:
                if ( arr[2] <= 15.500000000000002 ):
                    if ( arr[1] <= 14.500000000000002 ):
                        if ( arr[2] <= 1.5000000000000002 ):
                            return -1.315007272752868
                        else:
                            if ( arr[2] <= 4.500000000000001 ):
                                return -1.0751313995391458
                            else:
                                return -1.1918277702917675
                    else:
                        if ( arr[2] <= 1.0000000180025095e-35 ):
                            return -1.1737676176752903
                        else:
                            if ( arr[1] <= 70.50000000000001 ):
                                return -1.3717346752020594
                            else:
                                return -1.279350048356234
                else:
                    return -1.125144129861698
        else:
            return -1.354369143840062
    else:
        if ( arr[1] <= 13.500000000000002 ):
            if ( arr[1] <= 1.0000000180025095e-35 ):
                if ( arr[2] <= 5.500000000000001 ):
                    return -1.1043054922273012
                else:
                    if ( arr[0] <= 6.500000000000001 ):
                        return -1.130827394671079
                    else:
                        return -1.2501759556680785
            else:
                if ( arr[2] <= 2.5000000000000004 ):
                    return -1.2945713141065758
                else:
                    if ( arr[1] <= 2.5000000000000004 ):
                        return -1.2369150044461896
                    else:
                        return -1.118197917316899
        else:
            if ( arr[0] <= 7.500000000000001 ):
                if ( arr[0] <= 4.500000000000001 ):
                    return -1.130827394671079
                else:
                    return -1.0408835516008763
            else:
                return -1.17163032150766

```

## run test

```
pip install -r requirements-dev.txt

pytest tests
```

## extends and contribute

### support more LANGUAGE


### code style & static check

```
pre-commit run --all-files --show-diff-on-failure
```
