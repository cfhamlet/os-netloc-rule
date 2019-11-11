from .compat import iteritems
from .const import Symbols
from .utils import split_domain_port


class Node(object):
    __slots__ = ("_children", "_default_rule", "_port_rules")

    def __init__(self, port=None, rule=None):
        self._children = None
        self._default_rule = (-1, rule) if port == -1 else None
        self._port_rules = (port, rule) if port is not None and port != -1 else None

    def add_child(self, piece, port=None, rule=None, cmp=None):
        if self._children is None:
            self._children = (piece, Node(port, rule))
            return self._children[1]

        if isinstance(self._children, tuple):
            child = self._children[1]
            if piece == self._children[0]:
                child.add_rule(port, rule, cmp)
                return child
            new_child = Node(port, rule)
            self._children = {self._children[0]: self._children[1], piece: new_child}
            return new_child

        if piece not in self._children:
            child = Node(port, rule)
            self._children[piece] = child
            return child

        child = self._children[piece]
        child.add_rule(port, rule, cmp)
        return child

    def get_rule(self, port):
        rule = None
        match_port = False
        if self._port_rules is None:
            if self._default_rule is not None:
                rule = self._default_rule[1]
        elif isinstance(self._port_rules, tuple):
            if port == self._port_rules[0]:
                rule = self._port_rules[1]
                match_port = True
            elif self._default_rule is not None:
                rule = self._default_rule[1]
        else:
            if port in self._port_rules:
                rule = self._port_rules[port]
                match_port = True
            elif self._default_rule is not None:
                rule = self._default_rule[1]

        return rule, match_port

    def get_child(self, piece):
        if self._children is not None:
            if isinstance(self._children, tuple):
                if piece == self._children[0]:
                    return self._children[1]
            if piece in self._children:
                return self._children[piece]

    def match_child(self, piece):
        wildcard = exact = None
        if self._children is not None:
            if isinstance(self._children, tuple):
                if piece == self._children[0]:
                    exact = self._children[1]
                elif self._children[0] == Symbols.EMPTY:
                    wildcard = self._children[1]
            else:
                if Symbols.EMPTY in self._children:
                    wildcard = self._children[Symbols.EMPTY]
                if piece in self._children:
                    exact = self._children[piece]
        return wildcard, exact

    def add_rule(self, port, rule, cmp=None):
        if port is None:
            return
        elif port == -1:
            if self._default_rule is not None:
                if cmp is not None and self._default_rule[1] != rule:
                    rule = cmp(self._default_rule[1], rule)
            self._default_rule = (-1, rule)
        else:
            if self._port_rules is None:
                self._port_rules = (port, rule)
            elif isinstance(self._port_rules, tuple):
                if port == self._port_rules[0]:

                    if rule != self._port_rules[1]:
                        if cmp is not None:
                            rule = cmp(self._port_rules[1], rule)
                        self._port_rules = (port, rule)
                else:
                    self._port_rules = dict((self._port_rules, (port, rule)))
            elif port not in self._port_rules:
                self._port_rules[port] = rule
            else:
                if cmp is not None:
                    rule = cmp(self._port_rules[port], rule)
                self._port_rules[port] = rule


def load_from_pieces(root, pieces, port, rule, cmp=None):

    node = root
    if len(pieces) > 1:
        node = root.add_child(pieces[-1])

    for piece in pieces[-2:0:-1]:
        node = node.add_child(piece)

    node.add_child(pieces[0], port if port is not None else -1, rule, cmp=cmp)
    return root


def match_with_pieces(root, pieces, port):

    exact = root
    best_match = (None, None)  # rule, match_port

    for piece in pieces[::-1]:
        wildcard, exact = exact.match_child(piece)
        for node in (wildcard, exact):
            if node is not None:
                rule, match_port = node.get_rule(port)
                if not (best_match[1] and not match_port):
                    best_match = (rule, match_port)
        if exact is None:
            break
    return best_match[0]


def load(root, domain_with_port, rule, cmp=None):
    domain, port = split_domain_port(domain_with_port)
    return load_from_pieces(root, domain.split(Symbols.DOT), port, rule, cmp)


def match(root, domain_with_port):
    domain, port = split_domain_port(domain_with_port)
    return match_with_pieces(root, domain.split(Symbols.DOT), port)


# def delete(root, domain_with_port):
#     def _delete(node, pieces, port, idx):
#         piece = pieces[idx]
#         child = node.get_child(piece)
#         if child is None:
#             return False, None

#         if idx == 0:
#             rule, match_port = child.get_rule(port)

#         delete_and_rule = _delete(child, pieces, port, idx - 1)

#         if not delete_and_rule[0]:
#             return delete_and_rule

#         return delete_and_rule

#     domain, port = split_domain_port(domain_with_port)
#     pieces = domain.split(Symbols.DOT)

#     return _delete(root, pieces, port, len(pieces) - 1)


def dump(root):
    def _dump(node, pieces):
        if node._children is not None:
            if isinstance(node._children, tuple):
                piece, child = node._children
                pieces.append(piece)
                for r in _dump(child, pieces):
                    yield r
                pieces.pop(-1)
            else:
                for piece, child in iteritems(node._children):
                    pieces.append(piece)
                    for r in _dump(child, pieces):
                        yield r
                    pieces.pop(-1)

        if node._port_rules is not None:
            if isinstance(node._port_rules, tuple):
                port, rule = node._port_rules
                top = pieces[0]
                pieces[0] = Symbols.COLON.join((top, port))
                yield pieces, rule
                pieces[0] = top
            else:
                top = pieces[0]
                for port, rule in iteritems(node._port_rules):
                    pieces[0] = Symbols.COLON.join((top, port))
                    yield pieces, rule
                pieces[0] = top

        if node._default_rule is not None:
            yield pieces, node._default_rule[1]

    o = []
    for pieces, rule in _dump(root, o):
        yield Symbols.DOT.join(pieces[::-1]), rule
