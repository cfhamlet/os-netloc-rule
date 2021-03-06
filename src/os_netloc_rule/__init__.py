""" os-netloc-rule

A common library for netloc rule.
"""
import pkgutil
import sys

from .netloc import Matcher, Netloc

__all__ = ["__version__", "version_info", "Matcher", "Netloc"]


__version__ = pkgutil.get_data(__package__, "VERSION").decode("ascii").strip()
version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split("."))

if sys.version_info < (2, 7):
    sys.exit("os-netloc-rule %s requires Python 2.7+" % __version__)

del pkgutil
del sys
