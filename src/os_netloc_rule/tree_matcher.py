from .matcher import Matcher
from .netloc_reversed_tree import Node, delete, dump, load, match


class TreeMatcher(Matcher):
    def __init__(self):
        self._root = Node()

    def match(self, netloc):
        return match(self._root, netloc)

    def load(self, netloc, rule, cmp=None):
        return load(self._root, netloc, rule, cmp=cmp)

    def delete(self, netloc):
        return delete(self._root, netloc)

    def dump(self):
        for r in dump(self._root):
            yield r
