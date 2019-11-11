from .const import Symbols
from .netloc_reversed_tree import Node, load, match
from .utils import split_domain_port


class Matcher(object):
    def __init__(self):
        self._root = Node()

    def match(self, domain_with_port):
        return match(self._root, *split_domain_port(domain_with_port))

    def load(self, domain_with_port, rule, cmp=None):
        domain, port = split_domain_port(domain_with_port)
        return load(self._root, domain.split(Symbols.DOT), port, rule, cmp=cmp)
