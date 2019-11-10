from .netloc_reversed_tree import Node, load, match


class Matcher(object):
    def __init__(self):
        self._root = Node()

    def load(self, pieces, port, rule):
        return load(self._root, pieces, port, rule)

    def match(self, domain, port):
        return match(self._root, domain, port)
