import logging


def method_decorator(func):
    def wrapper(self, *argv, **kwargv):
        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        logging.info(func.__doc__)
        return func(self, *argv, **kwargv)
    return wrapper


class Something1(object):

    @method_decorator
    def method1(self):
        """documentation thru method decorator for method 1"""
        pass

    def method2(self):
        """documentation thru method decorator for method 2"""
        pass

    @method_decorator
    def method3(self):
        """documentation thru method decorator for method 3"""
        pass

s1 = Something1()
s1.method1()
s1.method2()
s1.method3()

# or thru class decorator


def class_decorator(cls):
    for name, method in cls.__dict__.iteritems():
        if not name.startswith('_'):
            setattr(cls, name, method_decorator(method))
    return cls


@class_decorator
class Something2(object):

    def method1(self):
        """documentation thru class decorator for method 1"""
        pass

    def method2(self):
        """documentation thru class decorator for method 2"""
        pass

    def method3(self):
        """documentation thru class decorator for method 3"""
        pass

s2 = Something2()
s2.method1()
s2.method2()
s2.method3()

# check mixed execution
s1.method1()
s2.method1()
