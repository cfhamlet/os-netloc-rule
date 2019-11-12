from __future__ import unicode_literals

import operator
import sys

_PY3 = sys.version_info[0] >= 3

if _PY3:
    iteritems = operator.methodcaller("items")

else:
    iteritems = operator.methodcaller("iteritems")
