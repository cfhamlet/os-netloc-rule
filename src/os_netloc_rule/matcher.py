from .netloc_reversed_tree import Node, load, match


class Matcher(object):
    def __init__(self):
        self._root = Node()

    def match(self, domain_with_port, schema=None):
        return match(self._root, domain_with_port, schema)

    def load(self, domain_with_port, rule, schema=None, cmp=None):
        return load(self._root, domain_with_port, rule, cmp=cmp)
