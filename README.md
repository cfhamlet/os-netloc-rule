# os-netloc-rule

[![Build Status](https://www.travis-ci.org/cfhamlet/os-netloc-rule.svg?branch=master)](https://www.travis-ci.org/cfhamlet/os-netloc-rule)
[![codecov](https://codecov.io/gh/cfhamlet/os-netloc-rule/branch/master/graph/badge.svg)](https://codecov.io/gh/cfhamlet/os-netloc-rule)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/os-netloc-rule.svg)](https://pypi.python.org/pypi/os-netloc-rule)
[![PyPI](https://img.shields.io/pypi/v/os-netloc-rule.svg)](https://pypi.python.org/pypi/os-netloc-rule)

A common library for netloc rule use case.


Netloc match is a very common and useful operation on processing URL. For example, netloc blacklist is a series rules of netloc with *ALLOWED* or *DISALLOWED*:

```
abc.example.com ALLOWED
.example.com DISALLOWED
```

You can skip processing ``http://www.example.com/001.html`` becase it match the rule ``.example.com DISALLOWED``.



## Install

```
pip install os-netloc-rule
```



## Usage

* load rule

    ```
    from os_netloc_rule import Matcher
    
    rules = [
        ('www.example.com', 1),
        ('abc.example.com', 2),
        ('abc.example.com:8080', 3),
    ]
    
    matcher = Matcher()
    for netloc, rule in rules:
        matcher.load(netloc, rule)
    ```

* match rule

    ```
    matcher.match('www.example.com')
    matcher.match('abc.example.com:8080')
    ```

* if there are same netloc with different rule,  the latter covers the former by default. But you can custom your own ``cmp`` function when loading rules

    ```
    def cmp(former, latter):
        return former if former > latter else latter
        
    matcher.load(netloc, rule, cmp=cmp)
    ```

## Unit Tests

```
tox
```

## License

MIT licensed.
