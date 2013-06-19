import logging
import unittest
import random
from functools import wraps


def method_decorator(func):
    @wraps(func)
    def wrapper(self, *argv, **kwargv):
        logging.basicConfig(filename='myapp.log',
                            level=logging.INFO, format='%(message)s')
        logging.info("\t- %s" % func.__doc__)
        return func(self, *argv, **kwargv)
    return wrapper


def class_decorator(cls):
    for name, method in cls.__dict__.iteritems():
        if not name.startswith('_'):
            setattr(cls, name, method_decorator(method))
    return cls


class MyTestingException(Exception):

    def __init__(self, value):
        self.msg = value

    def __str__(self):
        return "%s\n%s" % (self.msg, open("myapp.log").read())


@class_decorator
class Something(object):

    def _generate_number(self):
        if random.randint(0, 10) == 5:
            raise MyTestingException("Please have a look to details:")
        return random.randint(0, 2)

    def method1(self):
        """log to system to make some actions"""
        return self._generate_number()

    def method2(self):
        """registered account with additional credits"""
        return self._generate_number()

    def method3(self):
        """buy subscription for defined account"""
        return self._generate_number()


class TestSomething(unittest.TestCase):

    def setUp(self):
        with open("myapp.log", "w") as f:
            f.truncate()
        self.s = Something()
        self.data = {'some data': [1, 2, 3]}

    def test_method1(self):
        self.s.method1()
        self.s.method2()
        self.s.method3()
        self.assertEquals(self.s.method1(), 0)

    def test_method2(self):
        self.s.method3()
        self.s.method2()
        self.s.method1()
        self.assertEquals(self.s.method2(), 1)

    def test_method3(self):
        self.s.method1()
        self.s.method3()
        self.s.method2()
        self.assertEquals(self.s.method3(), 2)

if __name__ == '__main__':
    unittest.main()
