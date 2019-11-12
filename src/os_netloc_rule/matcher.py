from .netloc_reversed_tree import Node, delete, dump, load, match


class Matcher(object):
    def __init__(self):
        self._root = Node()

    def match(self, domain_with_port):
        return match(self._root, domain_with_port)

    def load(self, domain_with_port, rule, cmp=None):
        return load(self._root, domain_with_port, rule, cmp=cmp)

    def delete(self, domain_with_port):
        return delete(self._root, domain_with_port)

    def dump(self):
        for r in dump(self._root):
            yield r
