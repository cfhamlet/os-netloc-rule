# os-netloc-rule

[![Build Status](https://www.travis-ci.org/cfhamlet/os-netloc-rule.svg?branch=master)](https://www.travis-ci.org/cfhamlet/os-netloc-rule)
[![codecov](https://codecov.io/gh/cfhamlet/os-netloc-rule/branch/master/graph/badge.svg)](https://codecov.io/gh/cfhamlet/os-netloc-rule)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/os-netloc-rule.svg)](https://pypi.python.org/pypi/os-netloc-rule)
[![PyPI](https://img.shields.io/pypi/v/os-netloc-rule.svg)](https://pypi.python.org/pypi/os-netloc-rule)

A library for matching netloc.

Netloc is a concept to describe the location of a URL, it can be treated as 3-tuple (host, port, scheme)

Netloc match is a very common and useful operation on processing URL. For example, netloc blacklist is a series rules of netloc with *ALLOWED* or *DISALLOWED*:

```
abc.example.com|80|http ALLOWED
.example.com|| DISALLOWED
```

You can skip processing ``http://www.example.com/001.html`` becase it match ``.example.com|| DISALLOWED``.


## Install

```
pip install os-netloc-rule
```

## APIs

* load netloc and rule

    ```
    from os_netloc_rule import Matcher
    
    netloc_rules = [
        ('www.example.com||', 1),
        ('abc.example.com||', 2),
        ('abc.example.com|8080|', 3),
    ]
    
    matcher = Matcher()
    for netloc_string, rule in netloc_rules:
        matcher.load_from_string(netloc_string, rule)
    ```

* match netloc

    ```
    matcher.match('www.example.com')
    matcher.match('abc.example.com', '8080', 'http')
    ```

* if there are same netloc with different rule,  the latter covers the former by default. But you can custom your own ``cmp`` function when loading rules

    ```
    def cmp(former, latter):
        return -1 if former > latter else 1
        
    matcher.load(host, port, scheme, rule, cmp=cmp)
    ```

* iter netloc

    ```
    for netloc, rule in matcher.iter():
        pass
    ```

## Unit Tests

```
tox
```

## License

MIT licensed.
