import inspect
from functools import wraps


def initializer(func):

    spec = inspect.getfullargspec(func)

    @wraps(func)
    def wrapper(self, *args, **kargs):
        for name, arg in list(zip(spec.args[1:], args)) + list(kargs.items()):
            setattr(self, name, arg)
        func(self, *args, **kargs)

    return wrapper
